# -*- coding: utf-8 -*-
#
################################################################################
import sys
import collections
import re


# definition of token
Token = collections.namedtuple('Token', ('type', 'value', 'line', 'column'))

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
        ('tire', r'\u2013+'),                     # 
        ('MISMATCH', r'.'),                      # Any other character
    ],
    'second': [
        ('NUMBER', r'\d+(\.\d*)?'),              # Integer or decimal number
        ('WORD', r'[\w]+'),                      # words
        ('PUNCTUATION', r'[\.\,\;\:\!\?\'\"]'),  # punctuation
        ('NEWLINE', r'\n'),                      # Line endings
        ('SKIP', r'[ \t]+'),                     # Skip over spaces and tabs
        ('MISMATCH', r'.'),                      # Any other character
    ],
    'text': [
        ('NUMBER', r'\d+(\.\d*)?'),              # Integer or decimal number
        ('WORD', r'[\w]+'),                      # words
        ('PUNCTUATION', r'[\.\,\;\:\!\?\'\"]'),  # punctuation
        ('SYMBOL', r'[\-\+\*\\\/\=\&\%\$\~]'),             # symbols
        ('OPENBRACE', r'[\{\[\(]'),
        ('CLOSEBRACE', r'[\}\]\)]'),
        ('EOL', r'\n'),                      # Line endings
        ('SKIP', r'[ \t]+'),                     # Skip over spaces and tabs
        ('MISMATCH', r'.'),                      # Any other character
    ]
}


def tokenize(pattern, text):
    """
    Tokenizer function.

    Yields tokens.
        pattern - re.compile(...).
        text - text to tokenizing.
    """
    line_num = 1
    line_start = 0
    for mo in pattern.finditer(text):
        kind = mo.lastgroup
        value = mo.group(kind)
        if kind == 'EOL':
            column = mo.start() - line_start
            yield Token(kind, 'EOL', line_num, column)
            line_start = mo.end()
            line_num += 1
        elif kind == 'SKIP':
            pass
        elif kind == 'MISMATCH':
            # raise RuntimeError('%r unexpected on line %d' % (value, line_num))
            column = mo.start() - line_start
            yield Token('ERROR', value, line_num, column)
        else:
            column = mo.start() - line_start
            yield Token(kind, value, line_num, column)


def main(filename, ttable_key):
    """
    filename - file to lexing
    ttable_key - key in TOKENS_TABLE
    """
    fmt = "{type:<16} {value:<26} {line:0>5} {column:0>5}"
    if ttable_key in TOKENS_TABLE:
        tok_regex = '|'.join(['(?P<%s>%s)' % pair for pair in TOKENS_TABLE[ttable_key]])
        # pattern = re.compile(tok_regex, re.MULTILINE)
        pattern = re.compile(tok_regex)
        with open(filename, 'r', encoding='utf-8') as f:
            txt = ''.join(f.readlines())
        # header
        print('-' * 50)
        print('File: {0}, regexp: {1}'.format(filename, ttable_key))
        print('-' * 50)
        for token in tokenize(pattern, txt):
            print(fmt.format(type=token.type, value=token.value,
                             line=token.line, column=token.column))
    else:
        print('Key `{}` is absent in tokens table'.format(ttable_key))
        sys.exit(1)


if __name__ == "__main__":
    infomsg = """Usage:
       python3 {0} filename key -- do lexing filename with key from tokens table
       python3 {0} keys -- show keys from tokens table
    """
    # error using
    if len(sys.argv) < 2:
        print(infomsg.format(__file__))
        sys.exit(1)
    # show keys
    if len(sys.argv) == 2:
        if sys.argv[1] == 'keys':
            tkeys = sorted(TOKENS_TABLE.keys())
            print('Keys in tokens table: {}'.format(', '.join(tkeys)))
        else:
            print(infomsg.format(__file__))
            sys.exit(1)
    # do main program
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
