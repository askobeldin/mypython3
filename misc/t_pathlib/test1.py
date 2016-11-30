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

    info = '{msg:<18}:{value}'

    print(info.format(msg='Path(\'.\')', value=p1.resolve()))
    print(info.format(msg='Path(\'__file__\')', value=p2.resolve()))

    print(info.format(msg='p1.parent', value=p1.parent.resolve()))
    print(info.format(msg='p2.parent', value=p2.parent.resolve()))

    print(info.format(msg='p1.as_uri()', value=p1.resolve().as_uri()))
    print(info.format(msg='p2.as_uri()', value=p2.resolve().as_uri()))

    print(info.format(msg='Path.cwd()', value=Path.cwd()))

    print(info.format(msg='p1.is_dir()', value=p1.resolve().is_dir()))
    print(info.format(msg='p2.is_dir()', value=p2.resolve().is_dir()))

    print(info.format(msg='p1.is_file()', value=p1.resolve().is_file()))
    print(info.format(msg='p2.is_file()', value=p2.resolve().is_file()))

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
