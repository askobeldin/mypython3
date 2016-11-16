#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
###############################################################################
from collections import namedtuple
import string

__all__ = ['items']



# Returns True if textline consist from the same symbols and length > 3 symbols
def isline(textline):
    st = textline.strip()
    return all((len(set(st)) == 1, len(st) > 3))

# Returns True if textline is empty
isempty = lambda textline: len(textline.strip()) == 0

Item = namedtuple('Item', 'kind value')
"""
    Item('EMPTY', '') - empty text line
    Item('LINE', '=') - text line consists from `=` symbols
    Item('TEXT', 'This is a text') - it is a text line
"""

def items(filename, encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        for textline in f:
            line = textline.expandtabs(4)
            if isempty(line):
                yield Item(kind='EMPTY', value='')
            elif isline(line):
                yield Item(kind='LINE', value=line.strip()[0])
            else:
                yield Item(kind='TEXT', value=line)
