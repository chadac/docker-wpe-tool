#!/usr/bin/env python3

def short_help():
    return "Creates a new WPEngine install boilerplate."


def run(args):
    print("Initializing a WPEngine install...")

    if len(args) <= 1:
        install_dir = create_install_dir(*args)
    else:
        raise ValueError("Too many arguments supplied to 'wpe-tool init'.")

    wpe_config = create_wpe_config(install_dir)

    export_template(wpe_config)

    from lib import configure
    if configure.ask_yn("Pull assets from WPEngine via SFTP?"):
        wpe_secrets = create_wpe_secrets()
        init_db()
        init_wp_content()

    print("Finished!")


def create_install_dir(install_dir=None):
    import os, sys
    if not install_dir:
        try:
            install_dir = input("Installation directory: ")
        except KeyboardInterrupt:
            print()
            sys.exit()
    install_path = "volume/" + install_dir
    os.makedirs(install_path)
    os.chdir(install_path)
    return install_dir


def create_wpe_config(default_install_name=None):
    from lib import configure
    wpe_config = configure.init_config()
    configure.query_config(wpe_config, default_install_name)
    wpe_config.save()
    return wpe_config


def export_template(wpe_config):
    import os
    from string import Template
    substitutions = wpe_config.substitutions()
    for (dirpath, dirnames, filenames) in os.walk("/app/wp-template"):
        path = dirpath[17:]
        if not path:
            path = '.'
        if not os.path.exists(path):
            os.makedirs(path)
        for filename in filenames:
            source = dirpath + '/' + filename
            sink = path + '/' + filename
            with open(source, 'r') as f1:
                with open(sink, 'w') as f2:
                    content = f1.read()
                    template = Template(content)
                    new_content = template.substitute(**substitutions)
                    f2.write(new_content)


def create_wpe_secrets():
    from lib import configure
    wpe_secrets = configure.init_secrets()
    configure.query_secrets(wpe_secrets)
    wpe_secrets.save()
    return wpe_secrets


def init_db():
    from scripts.sftp import get_db
    get_db([], 'prod')


def init_wp_content():
    from scripts.sftp import get_folder
    get_folder('wp-content/plugins', 'prod')
    get_folder('wp-content/themes', 'prod')
