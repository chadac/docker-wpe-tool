#!/usr/bin/env python

import json
import itertools
import sys
import getpass


def init_settings():
    settings = Settings()
    settings.prod = Settings()
    settings.staging = Settings()
    return settings


def load_settings():
    pass


## Implementation from http://stackoverflow.com/a/23976949
class Settings:
    def __init__(self, **kwargs):
        self._data = dict()

    def __setitem__(self, key, value):
        self._data[key] = value

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
        return dict([(key, value._json) if isinstance(value, Settings) else (key, value) for (key, value) in self._data.items()])

    @property
    def _sub_settings(self):
        return [(key, value) for (key, value) in self._data.items() if isinstance(value, Settings)]

    @property
    def _sub_values(self):
        return [(key, value) for (key, value) in self._data.items() if not isinstance(value, Settings)]

    def substitutions(self, prefix=""):
        return dict([(prefix + key, value) for (key, value) in self._sub_values] +\
                    list(itertools.chain(*[value.substitutions(key + ".") for (key, value) in self._sub_settings])))

    def save(self):
        pass



def update(settings):
    print()
    print("## DOCKER")
    print()
    settings.virtual_hosts = input("Virtual host(s): ")
    settings.phpmyadmin_virtual_hosts = input("[PHPMyAdmin] Virtual Host: ")

    print()
    print("## WORDPRESS")
    print()
    settings.wp_db_charset = input("DB Charset: ")
    settings.wp_db_collate = input("DB Collation: ")
    settings.wp_table_prefix = input("Table Prefix: ")
    multisite_configs = ["single-site", "multisite-subdomain", "multisite-subfolder"]
    while True:
        print("Site configuration:")
        print(" [1] single-site")
        print(" [2] multisite-subdomain")
        print(" [3] multisite-subfolder")
        config_choice = input("Site configuration (1-3): ")
        if config_choice in ['1','2','3']:
            settings.wp_multisite_config = multisite_configs[int(config_choice)-1]
            break
        print("Error: Invalid choice. Please choose a value in {1,2,3}.")

    print()
    print("## WPENGINE SFTP")
    print()
    settings.sftp_url =  input("SFTP URL: ")
    settings.sftp_port = input("SFTP Port: ")
    settings.prod.sftp_username = input("[Production] SFTP Username: ")
    settings.prod.sftp_password = getpass.getpass("[Production] SFTP Password: ")
    settings.staging.sftp_username = input("[Staging] SFTP Username: ")
    settings.staging.sftp_password = getpass.getpass("[Stating] SFTP Password: ")

    print()
    print("## WPENGINE GIT")
    print()
    settings.prod.git_remote = input("[Production] Remote URL: ")
    settings.staging.git_remote = input("[Staging] Remote URL: ")


def run():
    import getpass
    from lib.settings import Settings
    print("Configuring your WP Engine connection...")

    settings = load_settings()

    try:
        update(settings)
    except KeyboardInterrupt:
        sys.exit()

    settings.save()


def help():
    pass
