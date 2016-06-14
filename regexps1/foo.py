# -*- coding: utf-8 -*-
#
################################################################################
import sys
import collections
import re


Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])
fmt = "{typ:<16} {value:<20} {line:0>5} {column:0>5}"

def tokenize(code):
    token_specification = [
        ('NUMBER', r'\d+(\.\d*)?'),              # Integer or decimal number
        ('WORD', r'[\w]+'),                      # words
        ('PUNCTUATION', r'[\.\,\;\:\!\?\'\"]'),  # punctuation
        ('SYMBOL', r'[\(\)\-\=\%]'),             # symbols
        ('BEGINSECTION', r'\{'),                 # {
        ('ENDSECTION', r'\}'),                   # }
        ('BEGINCOMMENT', r'\/\*'),               # /*
        ('ENDCOMMENT', r'\*\/'),                 # */
        ('IDMARKER', r'\|'),                     # |
        ('DESCRIPTION', r'\@'),                  # @
        ('NEWLINE', r'\n'),                      # Line endings
        ('SKIP', r'[ \t]+'),                     # Skip over spaces and tabs
        ('MISMATCH', r'.'),                      # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    line_num = 1
    line_start = 0
    pattern = re.compile(tok_regex)
    # for mo in re.finditer(tok_regex, code):
    for mo in pattern.finditer(code):
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
            column = mo.start() - line_start
            yield Token(kind, value, line_num, column)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print('Error: wrong using')
        sys.exit(1)
    else:
        argument = sys.argv[1]
        # print('Argument: {0}, type: {1}'.format(argument, type(argument)))
        with open(argument, "r", encoding="utf-8") as f:
            for line in f:
                for token in tokenize(line):
                    print(fmt.format(typ=token.typ,
                                     value=token.value,
                                     line=token.line,
                                     column=token.column))
