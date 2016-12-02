#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
###############################################################################
from collections import namedtuple
from itertools import count
import string

__all__ = ['items']


# Returns True if textline consists from one symbol, except whitespace
def _isline(textline):
    st = textline.strip()
    return all((len(set(st)) == 1,))

# Returns True if textline is empty
_isempty = lambda textline: len(textline.strip()) == 0

TextLine = namedtuple('TextLine', 'kind value linenr')
"""
    TextLine('EMPTY', '', 34) - empty text line
    TextLine('LINE', '=', 34) - text line consists from `=` symbols
    TextLine('TEXT', 'This is a text', 34) - it is a text line
"""

def items(filename, encoding='utf-8'):
    """Reads file `filename` with encoding `encoding` line by line and yielding
    TextLine item that describes the text line
    """
    with open(filename, 'r', encoding=encoding) as f:
        counter = count(start=1) # number of current text line
        for textline in f:
            nr = next(counter)
            line = textline.expandtabs(4)  # tab symbol = 4 spaces
            if _isempty(line):
                yield TextLine(kind='EMPTY', value='', linenr=nr)
            elif _isline(line):
                yield TextLine(kind='LINE', value=line.strip()[0], linenr=nr)
            else:
                yield TextLine(kind='TEXT', value=line, linenr=nr)
