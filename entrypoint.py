#!/usr/bin/env python

import os, sys
import argparse

parser = argparse.ArgumentParser(
    description="Tool for managing WPEngine installations.",
    usage="""wpe-tool <command> [<args>]

Commands:
  init        Initializes an empty WPEngine install
  configure   Reconfigures an existing WPEngine installation
  import-db   Imports the MySQL database from WPEngine SFTP servers
""")
parser.add_argument('command', type=str, help="""Command to run.""")

args = parser.parse_args(sys.argv[1:2])

import importlib

valid_commands = ["init", "configure", "import-db"]

if args.command in valid_commands:
    script = importlib.import_module('scripts.' + args.command)
    script.run(sys.argv[2:])
