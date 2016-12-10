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

    # do some work
    msg1 = '{nr: >4}  {kind:<22} {value!r}'
    msg2 = '{nr: >4} {shift:>3}  {kind:<22} {value!r}'
    for item in mymd.reader.items(arguments.datafile, encoding='utf-8'):
        if item.kind not in ('EMPTY', 'ERROR', 'LINE'):
            # try to count shift for text line
            m = re.search(r'\S', item.value)
            if m:
                shift = m.start()
            else:
                shift = None
            print(msg2.format(kind=item.kind,
                              value=item.value,
                              shift=shift,
                              nr=item.linenr))
        else:
            print(msg2.format(kind=item.kind,
                              value=item.value,
                              shift='-',
                              nr=item.linenr))


if __name__ == '__main__':
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)
