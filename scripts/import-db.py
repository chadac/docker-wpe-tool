#!/usr/bin/env python

import argparse

def _check_arg_environment(value):
    if value not in ["prod", "staging"]:
        raise argparse.ArgumentTypeError("Must specify either 'prod' or 'staging' for your environment (default: 'prod').")
    return value

def run(args):
    parser = argparse.ArgumentParser(
        description="Imports a MySQL database from the WPEngine SFTP endpoint.",
        usage="""
wpe-tool import-db <prod|staging>
""")
    parser.add_argument('environment', type=_check_arg_environment, help="The environment to pull the DB from.", default="prod")

    sargs = parser.parse_args(args)

    from lib import configure
    settings = configure.load_settings('/app/volume/wpe-config.json')
    secrets = configure.load_settings('/app/volume/wpe-secrets.json')
    sftp_cred = secrets._sub[sargs.environment]

    omysql = '/app/volume/.db/mysql.sql.original'
    nmysql = '/app/volume/.db/mysql.sql'

    print("Loading DB via SFTP...")
    import pysftp
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning, module='pysftp')
    hostname = settings['sftp_url']
    cnopts = pysftp.CnOpts()
    cnopts.hostkeys = None
    connection_args = {
        'host': settings['sftp_url'],
        'port': int(settings['sftp_port']),
        'username': sftp_cred['sftp_username'],
        'password': sftp_cred['sftp_password'],
        'cnopts': cnopts
    }
    with pysftp.Connection(**connection_args) as sftp:
        sftp.get(remotepath='wp-content/mysql.sql', localpath=omysql)

    import subprocess
    from urllib import parse

    remote_url = parse.urlparse(settings['wpe_prod_url'])
    remote_netloc = remote_url.netloc.replace('.', r'\.')

    print("Replacing with local URL...")
    subprocess.run(["cp", omysql, nmysql])

    # I use sed to do replacement rather than some of the other tools
    # available since the MySQL files can get very large and Python
    # doens't seem to have anything for re.sub on large files.
    commands = []
    if settings["wp_multisite_config"] == 'single-site' or settings["wp_multisite_config"] == 'multisite-subfolder':
        local_url = parse.urlparse(settings['virtual_hosts'])
        local_netloc = local_url.path.replace('.', r'\.')
        commands = [
            ["sed", "-i",
             r's/{}:\/\/{}/http:\/\/{}/g'.format(remote_url.scheme,
                                                 remote_netloc,
                                                 local_netloc),
             nmysql],
            ["sed", "-i",
             's/{}/{}/g'.format(remote_netloc, local_netloc),
             nmysql]
        ]
    elif settings["wp_multisite_config"] == 'multisite-subdomain':
        local_urls = [parse.urlparse(vh) for vh in settings['virtual_hosts'].split(',')]
        print(local_urls)
        local_netloc = local_urls[0].path.replace('.', r'\.')
        commands = [
            ["sed", "-i",
             r"s/{}:\/\/\([a-zA-Z0-9]\+\.\){}/http:\/\/\1{}/g".format(
                 remote_url.scheme, remote_netloc, local_netloc),
             nmysql],
            ["sed", "-i",
             r"s/\([a-zA-Z0-9]\+\.\){}/\1{}/g".format(
                 remote_netloc, local_netloc),
             nmysql]
        ]

    for command in commands:
        subprocess.run(command)
