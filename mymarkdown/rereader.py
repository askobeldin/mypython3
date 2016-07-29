# -*- coding: utf-8 -*-
#
################################################################################
"""
Читает файл и выдает блоки текста.
Блоки текста разделяются пустыми строками
"""

import sys
import re
import itertools
import argparse
import string
from collections import namedtuple

# from enum import Enum


# parts names of a document
# docitem = Enum('docitem', ('header',
                           # 'paragraph',
                           # 'image',
                          # ))


TEXTLINEINFO = namedtuple('TEXTLINEINFO', ('startswith', 'firstsymbol', 'shift'))

def textlineinfo(txtline):
    """
    возвращает именованный кортеж, описывающий некоторые параметры исследуемой
    строки txtline

    startswith - начальный символ строки
    firstsymbol - первый непробельный символ в строке
    shift - количество пробелов от начала строки до ее первого непробельного
    символа
    """
    firstsymbol = ''
    shift = 0
    startswith = txtline[0]
    for n, v in enumerate(txtline):
        if v in string.whitespace:
            shift = n
            continue
        if v in string.punctuation:
            shift = n
            firstsymbol = v
            break
        if v.isalnum():
            shift = n
            firstsymbol = v
            break
    return TEXTLINEINFO(startswith, firstsymbol, shift)

def rereader(infile, delimiter):
    """
    возвращает кортеж из строк блока текста

    блоки текста разделяется регулярным выражением delimiter

    при чтении файла, символы табуляции конвертируются в пробелы; длина одного
    символа - 4 пробела
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
    n = itertools.count(start=1)
    with open(datafile, 'r', encoding='utf-8') as f:
        blocks = rereader(f, empty_line)
        for b in blocks:
            # print('BLOCK {0:0>3}: {1}\n'.format(next(n), b), end='')
            print('[BLOCK {0:0>3}]:\n{1}'.format(next(n), ''.join(b)), end='')
            print('info -->:')
            for txtline in b:
                print(textlineinfo(txtline))
            print(80 * '=')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', help="Data file to read")
    arguments = parser.parse_args(sys.argv[1:])
    main(arguments.datafile)
