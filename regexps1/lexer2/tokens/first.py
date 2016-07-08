# -*- coding: utf-8 -*-
############################################################
# tokens table
TOKENS_TABLE = [
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
]

