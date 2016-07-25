# -*- coding: utf-8 -*-
#
################################################################################
"""
Читает файл и выдает блоки текста, разделенные пустыми строками
"""

import sys
import re
import argparse


def rereader(infile, delimiter):
    buf = []
    for tline in infile:
        if delimiter.match(tline):
            if not buf:
                pass
            else:
                yield ''.join(buf)
                buf.clear()
        else:
            buf.append(tline)
    if buf:
            yield ''.join(buf)
            buf.clear()


def main(datafile):
    empty_line = re.compile(r'\s*$')

    with open(datafile, 'r', encoding='utf-8') as f:
        blocks = rereader(f, empty_line)
        for i in blocks:
            print('BLOCK:\n{}\n\n'.format(i), end='')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', help="Data file to read")
    arguments = parser.parse_args(sys.argv[1:])
    main(arguments.datafile)
