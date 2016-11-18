# -*- coding: utf-8 -*-
#
###############################################################################
#
#

import unicodedata

chars = (
    '/',
    '\\',
    '+',
    '-',
    '*',
    '\'',
    '=',
    '3',
    'a',
    'Й',
    '\"',
    '&',
)

fmt = '{char:<5}{category:<4}{name:<60}'

for c in chars:
    name = unicodedata.name(c)
    print(fmt.format(name=name, char=c, category=unicodedata.category(c)))

