import getpass
def run(args):
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
