# -*- coding: utf-8 -*-
############################################################

# tokens table
TOKENS_TABLE = [
        ('NUMBER', r'\d+(\.\d*)?'),              # Integer or decimal number
        ('WORD', r'[\w]+'),                      # words
        ('PUNCTUATION', r'[\.\,\;\:\!\?\'\"]'),  # punctuation
        ('SYMBOL', r'[\-\+\*\\\/\=\&\%\$\~]'),             # symbols
        ('OPENBRACE', r'[\{\[\(]'),
        ('CLOSEBRACE', r'[\}\]\)]'),
        ('EOL', r'\n'),                      # Line endings
        ('SPACE', r'[ \t]'),                     # spaces and tabs
        ('MISMATCH', r'.'),                      # Any other character
]
