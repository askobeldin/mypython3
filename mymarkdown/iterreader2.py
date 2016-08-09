# -*- coding: utf-8 -*-
#
################################################################################
import sys
import re
import itertools
import argparse
# import string
from collections import namedtuple

# from rereader import textlineinfo


# tokens table
TOKENS_TABLE = (
        ('HEADER1', r'^#{1,6}\s?.+(?:\n|\r|\r\n?){2}(?im)'),
        ('HEADER2', r'^.+\s*(?:\n|\r|\r\n?)[\=|\-]{5,}(?:\n|\r|\r\n?){2}(?im)'),
        # ('EMPTYLINE', r'^\s*$(?m)'),
        ('UNORDEREDLISTITEM', r'^\s*(\-|\+|\*)\s+(.+(?:\n|\r|\r\n?))(?im)'),
        ('ORDEREDLISTITEM', r'^\s*\d+\.\d*\s+(.+(?:\n|\r|\r\n?))(?im)'),
        ('BLOCKQUOTEITEM', r'^\s*\>\s*?(.+(?:\n|\r|\r\n?))(?im)'),
        # it must be last; it can match empty text line
        ('TEXTITEM', r'(.+(?:\n|\r|\r\n?))+?(?im)'),
)

TOK_REGEX = '|'.join(['(?P<%s>%s)' % pair for pair in TOKENS_TABLE])
BLOCKSPATTERN = re.compile(TOK_REGEX)

BLOCK = namedtuple('BLOCK', ('type', 'value'))


def textblocks(txt):
    for mo in BLOCKSPATTERN.finditer(txt):
        kind = mo.lastgroup
        value = mo.group(kind)
        # print('[{}]:\n{!r}\n'.format(kind, value))
        yield BLOCK(kind, value)


def main(datafile):
    n = itertools.count(start=1)
    fmt1 = '[I] block: {block:0>3}, type: {type}\n{text}'
    with open(datafile, 'r', encoding='utf-8') as f:
        textlines = f.readlines()
    for block in textblocks(''.join(textlines)):
        # print(fmt1.format(block=next(n),
                          # type=block.type,
                          # text='{!r}'.format(block.value)))
        print(fmt1.format(block=next(n),
                          type=block.type,
                          text=block.value))
    # debugging
    # print('\n\ntxt is:\n{!r}'.format(txt))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', help="Text file to read")
    arguments = parser.parse_args(sys.argv[1:])
    main(arguments.datafile)
