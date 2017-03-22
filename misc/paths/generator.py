#! /usr/bin/env python3
# coding: utf-8
################################################################################
import sys
import os


def mkabspath(*chunks):
    items = list(chunks)
    return os.path.abspath(os.path.join(*items))

def main(curdir):
    # print(__file__)
    print('Current dir: {}'.format(curdir))
    foodir = mkabspath(curdir, 'foo')
    foofiles = os.listdir(path=foodir)
    for name in foofiles:
        apath = mkabspath(foodir, name)
        if os.path.isfile(apath):
            print('file: {}'.format(apath))
    

if __name__ == '__main__':
    rc = 1
    curdir = os.path.abspath(os.path.dirname(__file__))
    try:
        main(curdir)
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)

