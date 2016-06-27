# -*- coding: utf-8 -*-
#
################################################################################
from configparser import ConfigParser, ExtendedInterpolation
import re

parser = ConfigParser(interpolation=ExtendedInterpolation())
parser.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")
parser.read('config1.cfg', encoding='utf-8')

# column widths
columns = (22, 20, 50)

header_line = '|'.join(['{:^%s}' % i for i in columns])
data_line = '|'.join(['{:<%s}' % i for i in columns])

header = header_line.format('Section', 'Option', 'Value')
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
