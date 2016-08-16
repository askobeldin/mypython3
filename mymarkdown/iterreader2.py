# -*- coding: utf-8 -*-
#
################################################################################
import sys
import re
import itertools
import argparse
# import string
from collections import namedtuple
import io

# from rereader import textlineinfo


# tokens table
TOKENS_TABLE = (
        ('HEADER1', r'^#{1,6}\s?.+(?:\n|\r|\r\n?){1}(?im)'),
        ('HEADER2', r'^.+\s*(?:\n|\r|\r\n?)[\=|\-]{5,}(?:\n|\r|\r\n?){1}(?im)'),
        ('UNORDEREDLISTITEM', r'^[\t ]*?(\-|\+|\*)\s+(.+(?:\n|\r|\r\n?))(?im)'),
        ('ORDEREDLISTITEM', r'^[\t ]*?\d+\.\d*\s+(.+(?:\n|\r|\r\n?))(?im)'),
        ('BLOCKQUOTEITEM', r'^[\t ]*?\>\s*?(.+(?:\n|\r|\r\n?))(?im)'),
        ('EMPTYLINE', r'^\s*$'),
        # it must be last; it can match empty text line
        ('TEXTITEM', r'(.+(?:\n|\r|\r\n?)){1}(?im)'),
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


def main(arguments):
    n = itertools.count(start=1)
    fmt1 = '[I] block: {block:0>3}, type: {type}\n{text}'
    out = io.StringIO()
    with open(arguments.datafile, 'r', encoding='utf-8') as f:
        textlines = f.readlines()
    for block in textblocks(''.join(textlines)):
        if arguments.verbose:
            text = '{!r}'.format(block.value)
        else:
            text = block.value
        print(fmt1.format(block=next(n), type=block.type, text=text),
              file=out)
    print(out.getvalue())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', help="Text file to read")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Increase output verbosity")
    arguments = parser.parse_args(sys.argv[1:])
    main(arguments)
