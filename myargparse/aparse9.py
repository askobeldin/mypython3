# -*- coding: utf-8 -*-
############################################################
# see: http://jenyay.net/Programming/Argparse
#
#
import sys
import argparse


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count', default=1, type=int)
    return parser


if __name__ == '__main__':
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    # print('namespace is {}'.format(namespace))

    for _ in range(namespace.count):
        print("Привет, world! Epta!")
