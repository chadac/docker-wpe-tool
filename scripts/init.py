#!/usr/bin/env python

import os, sys
from string import Template

def run(args):
    print("Initializing a WPEngine install...")

    from lib import configure
    settings = configure.init_settings()

    try:
        install_dir_name = input("Installation directory: ")
        install_dir = "volume/" + install_dir_name
        configure.update(settings, install_dir_name)
    except KeyboardInterrupt:
        print()
        sys.exit()

    os.makedirs(install_dir)
    os.chdir(install_dir)

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
                    print(filename)
                    content = f1.read()
                    template = Template(content)
                    new_content = template.substitute(**settings.substitutions())
                    f2.write(new_content)

def help():
    pass
