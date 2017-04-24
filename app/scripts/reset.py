#!/usr/bin/env python3

## This is basically a clone of the init.py script.

def short_help():
    return "Resets a file that was previously provisioned using wpe-tool."

def run(args):
    import argparse
    parser = argparse.ArgumentParser(
        description=short_help(),
    )

    parser.add_argument('files', nargs='*', help='Files to reset.')
    parser.add_argument('--all', action='store_true', help='Resets all files in template')

    parsed_args = parser.parse_args(args)

    import os
    from lib import configure
    os.chdir('/app/volume')
    wpe_config = configure.load_config()
    substitutions = wpe_config.substitutions()

    if parsed_args.all:
        reset_all(substitutions)
    else:
        for filename in parsed_args.files:
            reset_file(filename, substitutions)

def reset_file(filename, substitutions):
    import os
    from string import Template
    local_file = '/app/volume/' + filename
    template_file = '/app/wp-template/' + filename
    with open(template_file, 'r') as f1:
        with open(local_file, 'w') as f2:
            content = f1.read()
            template = Template(content)
            new_content = template.substitute(**substitutions)
            f2.write(new_content)
            perms = os.stat(template_file).st_mode
            os.chmod(local_file, perms)

def reset_all(substitutions):
    import os
    for (dirpath, dirnames, filenames) in os.walk("/app/wp-template"):
        path = dirpath[17:]
        if not path:
            path = '.'
        local_path = '/app/volume/' + path
        if not os.path.exists(local_path):
            os.makedirs(local_path)
            perms = os.stat(dirpath).st_mode
            os.chmod(local_path, perms)
        for filename in filenames:
            reset_file(path + '/' + filename, substitutions)
