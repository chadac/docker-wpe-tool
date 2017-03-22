#!/usr/bin/env python3

def run(args):
    from lib import configure
    secrets = configure.update_secrets()
    secrets
