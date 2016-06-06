# -*- coding: utf-8 -*-
#
################################################################################
import collections
import re


Token = collections.namedtuple('Token', ['typ', 'value', 'line', 'column'])

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


statements = '''
/*
====================================
таблица 0.4
any comments go here

*/

@ type          table
@ Name  Таблица материалов
@ subtype       table to! 'html'
/* it would be better if description is on one line */
@ Description35  this is a description? three four five six seven


{|1| Стали углеродистые
	{ |10| Стали углеродистые, конструкционные
		{|12| с предельным содержанием углерода св. 0.1% до 0.24% включ. }
		{|14| с предельным содержанием углерода св. 0.24% до 0.35%  включ. }
		{|16| с предельным содержанием углерода св. 0.35% }
	}
	{ |30| Стали инструментальные углеродистые }
}

'''

fmt = "{typ:<16} {value:<20} {line:0>5} {column:0>5}"

for token in tokenize(statements):
    print(fmt.format(typ=token.typ,
                     value=token.value,
                     line=token.line,
                     column=token.column))
