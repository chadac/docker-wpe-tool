#!/usr/bin/env python

import json
import itertools
import sys
import getpass
from functools import reduce


def init_settings(filename):
    settings = Settings(filename)
    settings.add_subsetting('prod')
    settings.add_subsetting('staging')
    return settings


def init_config():
    return init_settings('wpe-config.json')


def init_secrets():
    return init_settings('wpe-secrets.json')


def load_config():
    return load_settings('wpe-config.json')


def load_secrets():
    return load_settings('wpe-secrets.json')


def load_settings(filename):
    try:
        with open(filename, 'r') as f:
            data = json.loads(f.read())
    except IOError as e:
        print("Could not find '{}': creating empty settings object.".format(filename))
        return init_settings(filename)
    return __load_settings(data, Settings(filename))


def __load_settings(data, settings=None):
    if settings == None:
        settings = Settings()
    for key, value in data.items():
        if isinstance(value, dict):
            settings.add_subsetting(key)
            __load_settings(value, settings._sub[key])
        else:
            settings._data[key] = value
    return settings


## Implementation loosely based on http://stackoverflow.com/a/23976949
class Settings:
    """Basic Settings object for general usage. Saves to a file."""
    def __init__(self, filename=None):
        self._data = dict()
        self._sub = dict()
        self.filename = filename

    def query(self, key, ask):
        value = ask()
        while value == False:
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
        """This is to be used with Python's templating library.

        Syntax:
          1. If 'key' has a string value, then it can be accessed with {{key}}
          2. If 'key' is a settings object with a key 'subkey', then it can be accessed with {{key__subkey}}
        """
        items = dict([(prefix + key, value) for (key, value) in self._data.items()])
        dicts = [value.substitutions(prefix + key + "__") for (key, value) in self._sub.items()]
        items = reduce(lambda x,y: {**x, **y}, [items] + dicts)
        return items

    def save(self):
        """Saves to a file"""
        with open(self.filename, 'w+') as f:
            f.write(json.dumps(self._json, indent=2))


################################################################
## HELPER METHODS
################################################################

def ask_yn(question, default='n'):
    result = ""
    while True:
        result = input(question + ' (y/n)' + (' (default: {})'.format(default) if default else '') + ': ')
        if result == "" and not default or not result in ['y','n','']:
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
    """Returns a function that will query the user to make a choice from
    several items.

    :param name: The label to appear before the query.
    :param choices: List of possible values to return.
    :param default: The default index choice to use.
    """
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
            return choices[int(result)-1]
    return ask

################################################################
## QUERY METHODS
################################################################

def query_config(settings, default_install_name=None):
    """Query generates a wpe_config object."""
    print()
    print("## WPENGINE")
    print()
    settings.query('wpe_install_name', _ask_text('Install Name', default_install_name))
    settings.prod.query('url', _ask_text('[Production] URL (include https://)', 'http://' + settings['wpe_install_name'] + '.wpengine.com'))
    settings.staging.query('url', _ask_text('[Staging] URL (include https://)', 'http://' + settings['wpe_install_name'] + '.staging.wpengine.com'))

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

def query_secrets(secrets):
    """Generates a wpe_secrets object."""
    if ask_yn("Add prod SFTP credentials?"):
        secrets.prod.query('sftp_username', _ask_text("[Production] SFTP Username"))
        secrets.prod.query('sftp_password', _ask_text("[Production] SFTP Password", input_method=getpass.getpass))
    if ask_yn("Add staging SFTP credentials?"):
        secrets.staging.query('sftp_username', _ask_text("[Staging] SFTP Username"))
        secrets.staging.query('sftp_password', _ask_text("[Staging] SFTP Username", input_method=getpass.getpass))
    if ask_yn("Add SSH credentials?"):
        secrets.query('ssh_id_rsa', _ask_text("SSH Private Key File", "~/.ssh/id_rsa"))
