#!/usr/bin/env python

## Entrypoint for the application.

import os, sys
import argparse
import glob, re, importlib

def import_scripts():
    """Identifies all scripts in the scripts/ folder. Each script is a
    Python module with an associated run() command that accepts
    multiple string arguments.

    """
    scripts = dict()
    for module_name in ['init', 'reconfigure', 'reset', 'sftp']:
        scripts[module_name] = importlib.import_module('scripts.' + module_name)
    return scripts

scripts = import_scripts()

usage="""wpe-tool <command> [<args>]

Commands:
"""
for command_name, module in scripts.items():
    usage += "   {:<15}  {}\n".format(command_name, module.short_help())

parser = argparse.ArgumentParser(
    description="Tool for managing WPEngine installations.",
    usage=usage
)

def script(name):
    """Checks if a script name is an actual script, returns the associated module."""
    if not name in scripts.keys():
        raise argparse.ArgumentTypeError("Invalid command.")
    return scripts[name]
parser.add_argument('command', type=script, help="""Command to run.""")
args = parser.parse_args(sys.argv[1:2])

args.command.run(sys.argv[2:])
