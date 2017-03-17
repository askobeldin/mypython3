# -*- coding: utf-8 -*-
#
###############################################################################
import sys
import re
import argparse
import os.path
import importlib

from functools import reduce
from operator import or_


def main(tmodule):
    matchmsg = 'regexp: |{}|, flags: {}\nmatches with: {!r}\n'
    matchmsg_grp = 'regexp: |{}|, flags: {}\nmatches with: {!r}\ngroups: {}\n'
    matchmsg_grpdict = 'regexp: |{}|, flags: {}\nmatches with: {!r}\ngroupdict: {}\n'
    doesntmatchmsg = '[-] regexp: |{}|, flags: {}\ndoesn\'t match with: {!r}\n'

    # for rexp, txt in tmodule.retable:
    for item in tmodule.retable:
        if (len(item) == 1) or (len(item) > 3):
            print('[E] Bad item in table: {}\n'.format(item))
            continue
        if len(item) == 2:
            rexp, txt = item
            flags = ''
            pattern = re.compile(rexp)
        if len(item) == 3:
            rexp, txt, flags = item
            pattern = re.compile(rexp,
                                 reduce(or_, [getattr(re, n) for n in flags]))
        match = pattern.match(txt)
        if match:
            mgroups = match.groups()
            mgroupdict = match.groupdict()
            if mgroups:
                if mgroupdict:
                    print(matchmsg_grpdict.format(rexp, flags, txt,
                                                  match.groupdict()))
                    continue
                print(matchmsg_grp.format(rexp, flags, txt, match.groups()))
            else:
                print(matchmsg.format(rexp, flags, txt))
        else:
            print(doesntmatchmsg.format(rexp, flags, txt))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', help="Data file")
    arguments = parser.parse_args(sys.argv[1:])
    tfile = os.path.normpath(arguments.datafile).replace('\\', '/')
    # prepare name of file for importing
    if tfile.endswith('.py'):
        tfile = tfile.replace('.py', '')
    if '/' in tfile:
        tfile = tfile.replace('/', '.')
    try:
        tt = importlib.import_module(tfile)
    except Exception:
        print('Importing {} error!'.format(tfile))
        sys.exit(1)
    main(tt)
