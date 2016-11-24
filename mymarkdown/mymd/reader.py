#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
###############################################################################
from collections import namedtuple
from itertools import count
import string

__all__ = ['items']


# Returns True if textline consist from the same symbols and length > 3 symbols
def _isline(textline):
    st = textline.strip()
    return all((len(set(st)) == 1, len(st) > 3))

# Returns True if textline is empty
_isempty = lambda textline: len(textline.strip()) == 0

Item = namedtuple('Item', 'kind value linenr')
"""
    Item('EMPTY', '', 34) - empty text line
    Item('LINE', '=', 34) - text line consists from `=` symbols
    Item('TEXT', 'This is a text', 34) - it is a text line
"""

def items(filename, encoding='utf-8'):
    """Reads file `filename` with encoding `encoding` line by line and yielding
    Item that describes a text line
    """
    with open(filename, 'r', encoding=encoding) as f:
        counter = count(start=1) # number of text line
        for textline in f:
            nr = next(counter)
            line = textline.expandtabs(4)
            if _isempty(line):
                yield Item(kind='EMPTY', value='', linenr=nr)
            elif _isline(line):
                yield Item(kind='LINE', value=line.strip()[0], linenr=nr)
            else:
                yield Item(kind='TEXT', value=line, linenr=nr)
