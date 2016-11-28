# -*- coding: utf-8 -*-
###############################################################################
import sys
#  import argparse
from pathlib import Path




def main(args=None):
    #  parser = argparse.ArgumentParser()
    #  parser.add_argument('folder',
                        #  help="Name of folder with markdown files")
    #  parser.add_argument('-e', '--extension',
                        #  default='*.md',
                        #  required=False,
                        #  help="Extension of markdown files")
    #  arguments = parser.parse_args(args)
    #  fn = filenames(arguments.folder, arguments.extension)

    p1 = Path('.')
    p2 = Path(__file__)

    msg1 = 'Path for \".\" is {}'
    msg2 = 'Path for \"__file__\" is {}'

    print(msg1.format(p1.resolve()))
    print(msg2.format(p2.resolve()))

    print('p1.parent is {}'.format(p1.parent.resolve()))
    print('p2.parent is {}'.format(p2.parent.resolve()))

    print('p1.as_uri() is {}'.format(p1.resolve().as_uri()))
    print('p2.as_uri() is {}'.format(p2.resolve().as_uri()))

    print('Path.cwd() is {}'.format(Path.cwd()))

    print('p1.is_dir() is {}'.format(p1.resolve().is_dir()))
    print('p2.is_dir() is {}'.format(p2.resolve().is_dir()))

    print('p1.is_file() is {}'.format(p1.resolve().is_file()))
    print('p2.is_file() is {}'.format(p2.resolve().is_file()))

    print('\n\np1.iterdir()\n==================================')
    for child in p1.iterdir():
        print(child.resolve())

    print('\n\np1.glob(*.py)\n==================================')
    for child in p1.glob('*.py'):
        print(child.resolve())

    print('\n\np1.rglob(*.py)\n==================================')
    for child in p1.rglob('*.py'):
        print(child.resolve())



if __name__ == '__main__':
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)
