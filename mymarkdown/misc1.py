# -*- coding: utf-8 -*-
#
################################################################################
import sys
import re
import itertools
import argparse
import string
from collections import namedtuple
import io

# from rereader import textlineinfo


# Returns True if textline consist from the same symbols
isline = lambda textline: len(set(textline.strip())) == 1

isempty = lambda textline: len(textline.strip()) == 0


def textlineinfo(textline):
    """возвращает кортеж, описывающий некоторые параметры исследуемой
    строки textline

    shift - количество пробелов от начала строки до ее первого непробельного
    символа
    firstsymbol - первый непробельный символ в строке
    """
    firstsymbol = ''
    shift = 0
    for n, v in enumerate(textline):
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
    return shift, firstsymbol


def main(arguments):
    n = itertools.count(start=1)
    info = ('[I] line: {line:<4} F: {first:<4} S: {shift:<3} '
            'empty?: {empty:<4} line?: {isline:<4}')
    fmt1 = info + '\n{text}'
    out = io.StringIO()
    with open(arguments.datafile, 'r', encoding='utf-8') as f:
        textlines = [line.expandtabs(4) for line in f.readlines()]
    for line in textlines:
        s, f = textlineinfo(line)
        isl = isline(line)
        if arguments.verbose:
            txt = '{!r}'.format(line)
        else:
            txt = line
        if arguments.info:
            outputline = info
        else:
            outputline = fmt1
        print(outputline.format(line=next(n),
                          first='{!r}'.format(f),
                          shift=s if s > 0 else '',
                          isline='T' if isl else '',
                          empty='T' if isempty(line) else '',
                          text=txt), file=out)
    print(out.getvalue())
    out.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', help="Text file to read")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Increase output verbosity")
    parser.add_argument('-i', '--info', action='store_true',
                        help="Prints just info")
    arguments = parser.parse_args(sys.argv[1:])
    main(arguments)
