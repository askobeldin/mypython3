# -*- coding: utf-8 -*-
#
################################################################################
import sys
import collections
import re
from glob import glob


# definition of token
Token = collections.namedtuple('Token', ['type', 'value', 'line', 'column'])

# tokens table
TOKENS_TABLE = {
    'first': [
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
    ],
    'second': [
        ('NUMBER', r'\d+(\.\d*)?'),              # Integer or decimal number
        ('WORD', r'[\w]+'),                      # words
        ('PUNCTUATION', r'[\.\,\;\:\!\?\'\"]'),  # punctuation
        ('NEWLINE', r'\n'),                      # Line endings
        ('SKIP', r'[ \t]+'),                     # Skip over spaces and tabs
        ('MISMATCH', r'.'),                      # Any other character
    ]
}

# names of files to lexing
FILENAMES = glob('*.dat')


def tokenize(pattern, text):
    line_num = 1
    line_start = 0
    for mo in pattern.finditer(text):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'NEWLINE':
            line_start = mo.end()
            line_num += 1
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            # raise RuntimeError('%r unexpected on line %d' % (value, line_num))
            print('ERROR: \"{0}\" unexpected on line {1}'.format(value, line_num))
            pass
        else:
            column = mo.start() - line_start
            yield Token(kind, value, line_num, column)


def main():
    fmt = "{type:<16} {value:<20} {line:0>5} {column:0>5}"
    for name in FILENAMES:
        with open(name, 'r', encoding='utf-8') as f:
            txt = ''.join(f.readlines())
            for key in TOKENS_TABLE:
                print('-' * 50)
                print('File: {0}, regexp: {1}'.format(name, key))
                print('-' * 50)
                tok_regex = '|'.join(['(?P<%s>%s)' % pair for pair in TOKENS_TABLE[key]])
                pattern = re.compile(tok_regex, re.MULTILINE)
                for token in tokenize(pattern, txt):
                    print(fmt.format(type=token.type,
                                     value=token.value,
                                     line=token.line,
                                     column=token.column))


if __name__ == "__main__":
    main()
