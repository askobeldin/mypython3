# -*- coding: utf-8 -*-
#
################################################################################
import string
from collections import namedtuple


TEXTLINEINFO = namedtuple('TEXTLINEINFO', ('startswith', 'firstsymbol', 'shift'))

def textlineinfo(txtline):
    firstsymbol = ''
    shift = 0
    startswith = txtline[0]
    for n, v in enumerate(txtline):
        if v in string.whitespace:
            shift = n
            continue
        if v in string.punctuation:
            shift = n
            firstsymbol = v
            break
        if v.isalnum():
            shift = n
            firstsymbol = v
            break
    return TEXTLINEINFO(startswith, firstsymbol, shift)
