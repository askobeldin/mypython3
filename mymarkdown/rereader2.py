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


TEXTLINEINFO = namedtuple('TEXTLINEINFO', ('firstsymbol', 'shift'))

def textlineinfo(txtline):
    """
    возвращает именованный кортеж, описывающий некоторые параметры исследуемой
    строки txtline

    firstsymbol - первый непробельный символ в строке
    shift - количество пробелов от начала строки до ее первого непробельного
    символа
    """
    firstsymbol = ''
    shift = 0
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
    return TEXTLINEINFO(firstsymbol, shift)


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
                # skip line
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
    fmt1 = '[I] block: {block:0>3}\n{text}'
    with open(datafile, 'r', encoding='utf-8') as f:
        blocks = rereader(f, empty_line)
        for b in blocks:
            print(fmt1.format(block=next(n),
                              text=''.join(b)))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', help="Data file to read")
    arguments = parser.parse_args(sys.argv[1:])
    main(arguments.datafile)
