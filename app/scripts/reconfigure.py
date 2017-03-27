def short_help():
    return "Reruns configuration tool for WPEngine configs."

def run(args):
    import argparse

    parser = argparse.ArgumentParser(
        description=short_help(),
        usage="""wpe-tool reconfigure <config>

Commands:
   wpe-config    The wpe-config.json file
   wpe-secrets   The wpe-secrets.json file
""")
    parser.add_argument('config', type=str, help='', default='wpe-config')
    parsed_args = parser.parse_args(args)

    config = parsed_args.config
    if config == 'wpe-config':
        wpe_config()
    elif config == 'wpe-secrets':
        wpe_secrets()
    else:
        raise argparse.ArgumentTypeError('Invalid config supplied.')


def wpe_config():
    from lib import configure
    wpe_config = configure.load_config()
    configure.update(wpe_config)
    wpe_config.save()


def wpe_secrets():
    from lib import configure
    wpe_secrets = configure.load_secrets()
    configure.update_secrets(wpe_secrets)
    wpe_secrets.save()
