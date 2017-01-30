# -*- coding: utf-8 -*-
#
###############################################################################
#
#

import sys
import unicodedata

names = (
    # http://www.unicode.org/Public/8.0.0/ucd/LineBreak.txt
    'EXCLAMATION MARK',
    'NUMBER SIGN',
    'COMMERCIAL AT',
    'CENT SIGN',
    'COPYRIGHT SIGN',
    'PLUS-MINUS SIGN',
    'CYRILLIC THOUSANDS SIGN',
    'ARABIC SEMICOLON',
    'ARABIC START OF RUB EL HIZB',
    'SYRIAC LETTER ALAPH',
    'BENGALI LETTER LA',

    # http://www.unicode.org/Public/8.0.0/ucd/NamesList.txt
    'GREEK SMALL LETTER IOTA WITH DIALYTIKA AND TONOS',
    'CYRILLIC CAPITAL LETTER YU',
    'CYRILLIC CAPITAL LETTER I WITH DIAERESIS',
    'ARMENIAN SMALL LETTER JHEH',
    'HEBREW LETTER FINAL TSADI',
    'ARABIC LETTER NOON',
    'GUJARATI LETTER NA',
    'LATIN CAPITAL LETTER L WITH DOT BELOW',
    'BALINESE LETTER RA',
    'HANGUL JUNGSEONG YEO',
)

if sys.platform.startswith('win'):
    outencoding = 'cp1251'
else:
    outencoding = 'utf-8'

fmt = '{name:<60}{char:<10}'

for n in names:
    tch = unicodedata.lookup(n)
    nch = unicodedata.normalize('NFC', tch)
    outstr = fmt.format(name=n, char=tch)
    # outstr = fmt.format(name=n, char=tch).encode(outencoding,
                                                 # errors='replace')
    print(outstr)
