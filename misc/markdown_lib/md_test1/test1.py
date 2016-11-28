# -*- coding: utf-8 -*-
###############################################################################
import sys
import argparse
from os.path import isdir, exists
from os.path import (abspath,
                     join,
                     basename,
                     splitext,
                     dirname,
                     expanduser)
from glob import glob

import markdown


def filenames(folder, extension):
    names = [path for path in glob(abspath(join(folder, extension)))]
    return [path for path in names if all((exists(path),))]

def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('folder',
                        help="Name of folder with markdown files")
    parser.add_argument('-e', '--extension',
                        default='*.md',
                        required=False,
                        help="Extension of markdown files")
    arguments = parser.parse_args(args)
    fn = filenames(arguments.folder, arguments.extension)
    mdc = markdown.Markdown(output_format='html5')
    for name in fn:
        text = ''
        with open(name, mode='r', encoding='utf-8') as f:
            text = f.read()
        html = mdc.convert(text)
        print('=====\nfile: {}\n====='.format(name))
        print(html)
        print()

if __name__ == '__main__':
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)
