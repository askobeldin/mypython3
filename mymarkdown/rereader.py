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

# XXX - not so good
def get_suggestions(txtblock):
    hints = []
    # headers or paragraphs?
    if len(txtblock) == 1:
        tlinfo = textlineinfo(txtblock[0])
        if tlinfo.firstsymbol in '#':
            hints.append('header')
    if len(txtblock) == 2:
        tlinfo = textlineinfo(txtblock[1])
        if tlinfo.firstsymbol in '-=':
            hints.append('header')
    # unorderd list
    tlinfo = textlineinfo(txtblock[0])
    if tlinfo.firstsymbol in '*-+':
        hints.append('unorderedlist')
    if tlinfo.shift > 0:
        hints.append('unorderedlist')

    # end of looking for suggestions
    if not hints:
        hints.append('paragraph')
    return set(hints)

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

def process_header(txt):
    """
    ((type, expr), ...)
    """
    result = ''
    headers = (
        # single line header
        ('h1', re.compile(r'^#{1}\s?(?P<text>\b.+\b)')),
        ('h2', re.compile(r'^#{2}\s?(?P<text>\b.+\b)')),
        ('h3', re.compile(r'^#{3}\s?(?P<text>\b.+\b)')),
        ('h4', re.compile(r'^#{4}\s?(?P<text>\b.+\b)')),
        ('h5', re.compile(r'^#{5}\s?(?P<text>\b.+\b)')),
        ('h6', re.compile(r'^#{6}\s?(?P<text>\b.+\b)')),
        # header on 2 lines
        ('h1', re.compile(r'(?P<text>\b.+\b)\s*?(?:\n|\r|\r\n?)\=+', re.MULTILINE)),
        ('h2', re.compile(r'(?P<text>\b.+\b)\s*?(?:\n|\r|\r\n?)\-+', re.MULTILINE)),
    )
    for t, e in headers:
        match = e.match(txt)
        if match:
            result = 'Header type {}, text: {!r}'.format(t, match.groupdict()['text'])
            break
    if not result:
        result = 'Header doesn\'t determined'
    return result


def main(datafile):
    empty_line = re.compile(r'\s*$')
    n = itertools.count(start=1)
    fmt1 = '[I] block: {block:0>3}, hints: {hints}\n{text}'
    with open(datafile, 'r', encoding='utf-8') as f:
        blocks = rereader(f, empty_line)
        for b in blocks:
            h = get_suggestions(b)
            # print(fmt1.format(block=next(n),
                              # hints=', '.join(str(i).upper() for i in h),
                              # text=''.join(b)))
            # check headers
            if 'header' in h:
                txt = ''.join(b)
                print('{}\n{!r}\n'.format(process_header(txt), txt))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', help="Data file to read")
    arguments = parser.parse_args(sys.argv[1:])
    main(arguments.datafile)
