# -*- coding: utf-8 -*-
#
###############################################################################
import sys
import argparse
import re

import mymd


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', help="Text file to read")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Increase output verbosity")
    parser.add_argument('-i', '--info', action='store_true',
                        help="Prints just info")
    arguments = parser.parse_args(args)
    # regexps
    # tokens table
    TOKENS_TABLE = (
            ('HEADER',
             r'^#{1,6}\s*.+(?:\n|\r|\r\n?)(?i)'),
            ('UNORDEREDLISTITEM',
             r'^\s*(\-|\+|\*)\s+(.+(?:\n|\r|\r\n?))(?i)'),
            ('ORDEREDLISTITEM',
             r'^\s*\d+\.\s+(.+(?:\n|\r|\r\n?))(?i)'),
            #  ('BLOCKQUOTEITEM', r'^[\t ]*?\>\s*?(.+(?:\n|\r|\r\n?))(?im)'),
            # it must be last; it can match empty text line
            ('TEXTITEM',
             r'(.+(?:\n|\r|\r\n?))(?i)'),
    )
    TOK_REGEX = '|'.join(['(?P<%s>%s)' % pair for pair in TOKENS_TABLE])
    BLOCKSPATTERN = re.compile(TOK_REGEX)

    # do some work
    msg1 = '{nr: >4}  {kind:<22}: {value!r}'
    for item in mymd.reader.items(arguments.datafile, encoding='utf-8'):
        if item.kind == 'TEXT':
            mo = re.match(BLOCKSPATTERN, item.value)
            if mo:
                kind = mo.lastgroup
                value = mo.group(kind)
                print(msg1.format(kind=kind,
                                  value=value, nr=item.linenr))
            else:
                print(msg1.format(kind='ERROR',
                                  value=item.value, nr=item.linenr))
        # item.kind == 'EMPTY' or 'LINE'
        else:
            print(msg1.format(kind=item.kind,
                              value=item.value, nr=item.linenr))


if __name__ == '__main__':
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)
