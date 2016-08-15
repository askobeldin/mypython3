# -*- coding: utf-8 -*-
#
################################################################################
import sys


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    print('Call MAIN function with args: {}'.format(args))
    # do some work
    import test1

    return 0
