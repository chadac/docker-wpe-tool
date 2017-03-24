#!/usr/bin/env python

import os, sys
import argparse
import glob, re, importlib

def import_scripts():
    scripts = dict()
    for module_name in ['init', 'reconfigure', 'sftp']:
        scripts[module_name] = importlib.import_module('scripts.' + module_name)
    return scripts

scripts = import_scripts()

usage="""wpe-tool <command> [<args>]

Commands:
"""
for command_name, module in scripts.items():
    usage += "   {:<10}  {}\n".format(command_name, module.short_help())

parser = argparse.ArgumentParser(
    description="Tool for managing WPEngine installations.",
    usage=usage
)

def script(name):
    if not name in scripts.keys():
        raise argparse.ArgumentTypeError("Invalid command.")
    return scripts[name]

parser.add_argument('command', type=script, help="""Command to run.""")

args = parser.parse_args(sys.argv[1:2])

args.command.run(sys.argv[2:])
