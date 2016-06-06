# -*- coding: utf-8 -*-
#
################################################################################
import collections
import re


Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])

def tokenize(code):
    keywords = {'IF', 'THEN', 'ENDIF', 'FOR', 'NEXT', 'GOSUB', 'RETURN'}
    token_specification = [
        ('NUMBER',   r'\d+(\.\d*)?'), # Integer or decimal number
        ('ASSIGN',   r':='),          # Assignment operator
        ('END',      r';'),           # Statement terminator
        ('ID',       r'[A-Za-z]+'),   # Identifiers
        ('OP',       r'[+\-*/]'),     # Arithmetic operators
        ('NEWLINE',  r'\n'),          # Line endings
        ('SKIP',     r'[ \t]+'),      # Skip over spaces and tabs
        ('MISMATCH', r'.'),           # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    # tok_regex =>
    # '(?P<NUMBER>\\d+(\\.\\d*)?)|(?P<ASSIGN>:=)|(?P<END>;)|(?P<ID>[A-Za-z]+)|
    #  (?P<OP>[+\\-*/])|(?P<NEWLINE>\\n)|(?P<SKIP>[ \\t]+)|(?P<MISMATCH>.)'
    line_num = 1
    line_start = 0
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            raise RuntimeError('%r unexpected on line %d' % (value, line_num))
        else:
            if kind == 'ID' and value in keywords:
                kind = value
            column = mo.start() - line_start
            yield Token(kind, value, line_num, column)


statements = '''
    IF quantity THEN
        total := total + price * quantity;
        tax := price * 0.05;
        tax:=price*0.05;
    ENDIF;
'''

for token in tokenize(statements):
    print(token)

"""
Token(typ='IF', value='IF', line=2, column=4)
Token(typ='ID', value='quantity', line=2, column=7)
Token(typ='THEN', value='THEN', line=2, column=16)
Token(typ='ID', value='total', line=3, column=8)
Token(typ='ASSIGN', value=':=', line=3, column=14)
Token(typ='ID', value='total', line=3, column=17)
Token(typ='OP', value='+', line=3, column=23)
Token(typ='ID', value='price', line=3, column=25)
Token(typ='OP', value='*', line=3, column=31)
Token(typ='ID', value='quantity', line=3, column=33)
Token(typ='END', value=';', line=3, column=41)
Token(typ='ID', value='tax', line=4, column=8)
Token(typ='ASSIGN', value=':=', line=4, column=12)
Token(typ='ID', value='price', line=4, column=15)
Token(typ='OP', value='*', line=4, column=21)
Token(typ='NUMBER', value='0.05', line=4, column=23)
Token(typ='END', value=';', line=4, column=27)
Token(typ='ENDIF', value='ENDIF', line=5, column=4)
Token(typ='END', value=';', line=5, column=9)
"""









"""
####################################################
определения в моем старом токенайзере:

scanner = re.Scanner([
    (r'[\-\.\,\;\%\(\)\w]+',  lambda scanner, token: ('WORD', token)),
    (r'\{',                   lambda scanner, token: ('BEGINSECTION', token)),
    (r'\}',                   lambda scanner, token: ('ENDSECTION', token)),
    (r'\/\*',                 lambda scanner, token: ('BEGINCOMMENT', token)),
    (r'\*\/',                 lambda scanner, token: ('ENDCOMMENT', token)),
    (r'\@',                   lambda scanner, token: ('DESCRIPTION', token)),
    (u'.',                    None)],
    re.UNICODE)

"""
