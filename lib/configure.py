#!/usr/bin/env python

import json
import itertools
import sys
import getpass
from functools import reduce


def init_settings():
    settings = Settings()
    settings.add_subsetting('prod')
    settings.add_subsetting('staging')
    return settings


def load_settings(filename):
    with open(filename, 'w') as f:
        data = json.loads(f.read())
    return __load_settings(data)


def __load_settings(data, settings=None):
    if not settings:
        settings = None
    for key, value in data.items():
        if isinstance(value, dict):
            settings.add_subsetting(key)
            __load_settings(value, settings._sub[key])
        else:
            settings._data[key] = value
    return settings

## Implementation from http://stackoverflow.com/a/23976949
class Settings:
    def __init__(self, **kwargs):
        self._data = dict()
        self._sub = dict()

    def query(self, key, ask):
        value = ask()
        while value == None:
            value = ask()
        self._data[key] = value

    def add_subsetting(self, key):
        self.__dict__[key] = Settings()
        self._sub[key] = self.__dict__[key]

    def __getitem__(self, key):
        return self._data[key]

    def __repr__(self):
        return repr(self._json)

    def __len__(self):
        return len(self._json)

    def __delitem__(self, key):
        del self._validate[key]
        del self._data[key]

    def __contains__(self, key):
        return key in self._data

    @property
    def _json(self):
        sub_json = {key:sub._json for (key, sub) in self._sub.items()}
        return {**self._data, **sub_json}

    def substitutions(self, prefix=""):
        items = dict([(prefix + key, value) for (key, value) in self._data.items()])
        dicts = [value.substitutions(prefix + key + "__") for (key, value) in self._sub.items()]
        items = reduce(lambda x,y: {**x, **y}, [items] + dicts)
        return items

    def save(self, filename):
        with open(filename, 'w') as f:
            f.write(json.dumps(self._json, indent=2))

def ask_yn(question, default='n'):
    result = ""
    while True:
        result = input(question + ' (y/n)' + (' (default: {})' if default else '') + ': ')
        if result == "" and not default or not result in ['y','n']:
            print("Choose either 'y' or 'n'.")
        else:
            break
    return result == 'y'

def _ask_text(name, default=None, input_method=input):
    def ask():
        result = input_method(name + ' ' + ("(default: '{}')".format(default) if not default == None else '(required)') + ': ')
        if result == "" and default == None:
            print("** ERROR: A value is required for field '" + name + "'. **")
            return False
        elif result == "":
            return default
        else:
            return result
    return ask


def _ask_choice(name, choices, default=None):
    def ask():
        print("Choices:")
        for index, choice in enumerate(choices):
            print(" [{}] {}".format(index+1, choice))
        result = _ask_text(name, str(default))()
        if result == False:
            return False
        elif result not in map(lambda x: str(x+1), range(len(choices))):
            print("ERROR: Invalid choice. Please give a value in the range 1-{}".format(len(choices)))
            return False
        else:
            return choices[int(result)]
    return ask


def update(settings, default_install_name=None):
    print()
    print("## WPENGINE")
    print()
    settings.query('wpe_install_name', _ask_text('Install Name', default_install_name))
    settings.query('wpe_prod_url', _ask_text('Production URL (include https://)', 'https://' + settings['wpe_install_name'] + '.wpengine.com'))

    print()
    print("## DOCKER")
    print()
    settings.query('virtual_hosts', _ask_text("Virtual host(s)"))
    settings.query('phpmyadmin_virtual_host', _ask_text("[PHPMyAdmin] Virtual Host"))

    print()
    print("## WORDPRESS")
    print()
    settings.query('wp_db_charset', _ask_text("DB Charset", 'utf8'))
    settings.query('wp_db_collate', _ask_text("DB Collation", ''))
    settings.query('wp_table_prefix', _ask_text("Table Prefix", "wp_"))
    settings.query('wp_multisite_config', _ask_choice("Site Configuration", ["single-site", "multisite-subdomain", "multisite-subfolder"], 1))

    print()
    print("## WPENGINE SFTP")
    print()
    settings.query('sftp_url', _ask_text("SFTP URL", settings['wpe_install_name'] + '.sftp.wpengine.com'))
    settings.query('sftp_port', _ask_text("SFTP Port", '2222'))

    print()
    print("## WPENGINE GIT")
    print()
    settings.prod.query('git_remote', _ask_text("[Production] Remote URL", "git@git.wpengine.com:production/" + settings['wpe_install_name']))
    settings.staging.query('git_remote', _ask_text("[Staging] Remote URL", "git@git.wpengine.com:staging/" + settings['wpe_install_name']))

def update_secrets(secrets):
    if ask_yn("Add prod SFTP credentials?"):
        secrets.prod.query('sftp_username', _ask_text("[Production] SFTP Username"))
        secrets.prod.query('sftp_password', _ask_text("[Production] SFTP Password", input_method=getpass.getpass))
    if ask_yn("Add staging SFTP credentials?"):
        secrets.staging.query('sftp_username', _ask_text("[Staging] SFTP Username"))
        secrets.staging.query('sftp_password', _ask_text("[Staging] SFTP Username", input_method=getpass.getpass))
    if ask_yn("Add SSH credentials?"):
        secrets.query('ssh_id_rsa', _ask_text("SSH Private Key File", "~/.ssh/id_rsa"))
