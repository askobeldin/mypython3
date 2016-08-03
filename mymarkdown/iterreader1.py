# -*- coding: utf-8 -*-
#
################################################################################
import sys
import re
import itertools
import argparse
import string
from collections import namedtuple

# tokens table
TOKENS_TABLE = (
        ('HEADER1', r'^#{1,6}\s?.+(?:\n|\r|\r\n?){2}(?m)'),
        ('HEADER2', r'^.+\s*(?:\n|\r|\r\n?)[\=|\-]{5,}(?:\n|\r|\r\n?){2}(?m)'),
        # ('EMPTYLINE', r'^\s*$(?m)'),
        ('TEXTBLOCK', r'(.+(?:\n|\r|\r\n?))+(?m)'),
)

def main(datafile):
    with open(datafile, 'r', encoding='utf-8') as f:
        txt = ''.join(f.readlines())
    tok_regex = '|'.join(['(?P<%s>%s)' % pair for pair in TOKENS_TABLE])
    pattern = re.compile(tok_regex)
    for mo in pattern.finditer(txt):
        kind = mo.lastgroup
        value = mo.group(kind)
        print('[{}]:\n{}'.format(kind, value))
    # debugging
    # print('\n\ntxt is:\n{!r}'.format(txt))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', help="Text file to read")
    arguments = parser.parse_args(sys.argv[1:])
    main(arguments.datafile)
