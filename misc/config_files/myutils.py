# -*- coding: utf-8 -*-
#
################################################################################

# columns
# ((w1, name1), (w2, name2), ...)
columns = ((22, 'Section'), (20, 'Option'), (70, 'Value'))


header_line = '|'.join(['{:^%s}' % w for w, __ in columns])
data_line = '|'.join(['{:<%s}' % w for w, __ in columns])
header = header_line.format(*[name for __, name in columns])



def showconfig1(parser):
    print('-' * len(header))
    print(header)
    print('-' * len(header))

    for section in parser.sections():
        for option in parser.options(section):
            value = parser.get(section, option, fallback="---")
            # multiline values
            if '\n' in value:
                value = ', '.join([word for word in value.split('\n') if word])
            print(data_line.format(section, option, value))

