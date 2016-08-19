# -*- coding: utf-8 -*-
#
################################################################################
import sys
import argparse
import io

import mdreader


def main(arguments):
    # with io.StringIO() as out:
        # for i in mdreader.items(arguments.datafile):
            # print(i, file=out)
        # print(out.getvalue())
    c = mdreader.MDConverter(arguments.datafile)
    print(c.astextfile())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', help="Text file to read")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Increase output verbosity")
    parser.add_argument('-i', '--info', action='store_true',
                        help="Prints just info")
    arguments = parser.parse_args(sys.argv[1:])
    main(arguments)
