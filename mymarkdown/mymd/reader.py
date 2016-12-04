#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
###############################################################################
from collections import namedtuple
from itertools import count
import string
import re

__all__ = ['items']


# tokens table
_TOKENS = (
        ('HEADER',
         r'^#{1,6}\s*.+(?:\n|\r|\r\n?)(?i)'),
        ('UNORDEREDLISTITEM',
         r'^\s*(\-|\+|\*)\s+(.+(?:\n|\r|\r\n?))(?i)'),
        ('ORDEREDLISTITEM',
         r'^\s*\d+\.\s+(.+(?:\n|\r|\r\n?))(?i)'),
        ('BLOCKQUOTEITEM',
         r'^\s*\>\s*(.+(?:\n|\r|\r\n?))(?i)'),
        ('REFLINKITEM',
         r'^\s*\[.+\]\:(.+(?:\n|\r|\r\n?))(?i)'),
        # it must be last
        ('TEXTITEM',
         r'(.+(?:\n|\r|\r\n?))(?i)'),
)

_TOK_REGEX = '|'.join(['(?P<%s>%s)' % pair for pair in _TOKENS])
_BLOCKSPATTERN = re.compile(_TOK_REGEX)

# Returns True if textline consists from one symbol, except whitespace
def _isline(textline):
    st = textline.strip()
    return all((len(set(st)) == 1,))

# Returns True if textline is empty
_isempty = lambda textline: len(textline.strip()) == 0

#  TextLine = namedtuple('TextLine', 'kind value linenr')
"""
    TextLine('EMPTY', '', 34) - empty text line
    TextLine('LINE', '=', 34) - text line consists from `=` symbols
    TextLine('TEXT', 'This is a text', 34) - it is a text line
"""

class TextLine:
    __slots__ = ('kind', 'value', 'linenr')
    def __init__(self, kind, value, linenr):
        self.kind = kind
        self.value = value
        self.linenr = linenr

def items(filename, encoding='utf-8'):
    """Reads file `filename` with encoding `encoding` line by line and yielding
    TextLine item that describes the text line
    """
    with open(filename, 'r', encoding=encoding) as f:
        counter = count(start=1) # number of current text line
        for textline in f:
            nr = next(counter)
            line = textline.expandtabs(4)  # tab symbol = 4 spaces
            # empty text line?
            if _isempty(line):
                yield TextLine(kind='EMPTY', value='', linenr=nr)
            # text line from the same symbols
            elif _isline(line):
                yield TextLine(kind='LINE', value=line.strip()[0], linenr=nr)
            # valid text line
            else:
                #  yield TextLine(kind='TEXT', value=line, linenr=nr)
                mo = re.match(_BLOCKSPATTERN, line)
                if mo:
                    kind = mo.lastgroup
                    value = mo.group(kind)
                    yield TextLine(kind=kind, value=value, linenr=nr)
                # error
                else:
                    yield TextLine(kind='ERROR', value=value, linenr=nr)
