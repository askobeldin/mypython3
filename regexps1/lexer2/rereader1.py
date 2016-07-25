# -*- coding: utf-8 -*-
#
################################################################################
"""
Читает файл и выдает блоки текста.
Блоки текста разделяются пустыми строками
"""

import sys
import re
import argparse


def rereader(infile, delimiter):
    """
    возвращает кортеж из строк блока текста
    """
    buf = []
    for tline in infile:
        tline = tline.expandtabs(tabsize=4)
        if delimiter.match(tline):
            if not buf:
                # skip empty lines
                pass
            else:
                yield tuple(buf)
                buf.clear()
        else:
            buf.append(tline)
    if buf:
            yield tuple(buf)
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
