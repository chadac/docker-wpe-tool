#!/usr/bin/env python

import os, sys
from string import Template

def run(args):
    print("Initializing a WPEngine install...")

    from scripts import configure
    settings = configure.init_settings()


    try:
        install_dir = "volume/" + input("Installation directory: ")

        configure.update(settings)
    except KeyboardInterrupt:
        sys.exit()

    print(settings.substitutions())
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
                    content = f1.read()
                    template = Template(content)
                    new_content = template.substitute(**settings.substitutions())
                    f2.write(new_content)

def help():
    pass
