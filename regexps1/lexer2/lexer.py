# -*- coding: utf-8 -*-
#
################################################################################
import sys
import collections
import re
import importlib
import argparse


# definition of token
Token = collections.namedtuple('Token', ('type', 'value', 'line', 'column'))

"""
Попытка изменить логику работы скрипта

запуск:
    python3 lexer.py data/one.dat tokens/text.py

    data/one.dat -- file with text to lexing
    tokens/text.py -- text.py in dir `tokens`, it has TOKENS_TABLE
"""


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
        elif kind == 'SPACE':
            column = mo.start() - line_start
            yield Token(kind, ' ', line_num, column)
        elif kind == 'MISMATCH':
            # raise RuntimeError('%r unexpected on line %d' % (value, line_num))
            column = mo.start() - line_start
            yield Token('ERROR', value, line_num, column)
        else:
            column = mo.start() - line_start
            yield Token(kind, value, line_num, column)


def main(filename, ttable):
    """
    filename - file to lexing
    ttable - tokens table
    """
    fmt = "{type:<16} {value:<26} {line:0>5} {column:0>5}"
    tok_regex = '|'.join(['(?P<%s>%s)' % pair for pair in ttable])
    # pattern = re.compile(tok_regex, re.MULTILINE)
    pattern = re.compile(tok_regex)
    with open(filename, 'r', encoding='utf-8') as f:
        txt = ''.join(f.readlines())
    # header
    print('-' * 50)
    print('File: {0}'.format(filename))
    print('-' * 50)
    for token in tokenize(pattern, txt):
        print(fmt.format(type=token.type, value=token.value,
                         line=token.line, column=token.column))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('datafile', help="Data file to lexing")
    parser.add_argument('tokensfile', help="File with tokens table")
    arguments = parser.parse_args(sys.argv[1:])

    tfile = arguments.tokensfile

    # prepare name of tokensfile for importing
    if tfile.endswith('.py'):
        tfile = tfile.replace('.py', '')
    if '/' in tfile:
        tfile = tfile.replace('/', '.')
    try:
        tt = importlib.import_module(tfile)
    except Exception:
        print('Import {} error!'.format(tfile))
        sys.exit(1)
    main(arguments.datafile, tt.TOKENS_TABLE)
