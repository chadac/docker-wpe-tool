#!/usr/bin/env python3

def run(args):
    from lib import configure
    secrets = configure.load_settings('/app/volume/wpe-secrets.json')
    configure.update_secrets(secrets)
    secrets.save("/app/volume/wpe-secrets.json")
