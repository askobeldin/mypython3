# -*- coding: utf-8 -*-
#
###############################################################################
import sys
import argparse
from enum import Enum

import mymd


# возможные сигналы для обработки КА
labels = Enum('labels', ['TEXTITEM',
                         'LINE',
                         'EMPTY',
                         'HEADER',
                         'ORDEREDLISTITEM',
                         'UNORDEREDLISTITEM',
                         'REFLINKITEM',
                        ])

# possible states of FSM
states = Enum('states', ['I',   # initial state
                         'RP',  # read a paragraph
                         'RHL', # read a header with line
                         'ROL', # read ordered list
                         'RUL', # read unordered list
                         'RH',  # read a one line header
                        ])

# таблица переходов КА
transition_table = (
    (states.I, labels.EMPTY, states.I),
    (states.I, labels.HEADER, states.RH),
    (states.RH, '*', states.I),
)



def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', help="Text file to read")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Increase output verbosity")
    parser.add_argument('-i', '--info', action='store_true',
                        help="Prints just info")
    arguments = parser.parse_args(args)

    # do some work
    c = mymd.Convertor()
    tpl = c.convertfile(arguments.datafile, encoding='utf-8')
    # items in tpl are: (linenr as int, kind as str, value as str)
    print(tpl)


if __name__ == '__main__':
    rc = 1
    try:
        main()
        rc = 0
    except Exception as e:
        print('Error: %s' % e, file=sys.stderr)
    sys.exit(rc)
