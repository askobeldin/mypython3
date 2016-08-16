# -*- coding: utf-8 -*-
############################################################
from configparser import ConfigParser, ExtendedInterpolation
import re
from os.path import isdir, exists
from os.path import (abspath,
                     join,
                     basename,
                     splitext,
                     dirname,
                     expanduser)
from glob import glob
import sys
from types import ModuleType


print('__name__ is {}'.format(__name__))
print('__file__ is {}'.format(abspath(__file__)))
print('os.path.dirname is {}'.format(dirname(abspath(__file__))))
print('home folder is {}'.format(expanduser('~')))

pconfig = ConfigParser(interpolation=ExtendedInterpolation())
pconfig.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")
pconfig.read('config1.cfg', encoding='utf-8')

############################
# pretty output
#
# column widths
columns = (20, 20, 50)

header_line = '|'.join(['{:^%s}' % i for i in columns])
data_line = '|'.join(['{:<%s}' % i for i in columns])

header = header_line.format('Section', 'Option', 'Value')
print('-' * len(header))
print(header)
print('-' * len(header))

for section in pconfig.sections():
    for option in pconfig.options(section):
        value = pconfig.get(section, option, fallback="---") # ???
        # multiline values
        if '\n' in value:
            value = ', '.join([word for word in value.split('\n') if word])
        print(data_line.format(section, option, value))
############################
def cmdfiles(folder):
    names = [path for path in glob(abspath(join(folder, '*.py')))]
    return [path for path in names if all((exists(path),
                                           not basename(path).startswith('_')))]


cmds = cmdfiles(pconfig[sys.platform]['cli_commands'])
print('\nCommands: {}'.format(', '.join([name for name, ext in
                                       [splitext(basename(c)) for c in
                                        cmds]])))

cmd_items = []
for c in cmds:
    name, ext = splitext(basename(c))
    cmd_items.append((name, c))

# class for dynamic creation of methods
class NS: pass
NS.x = 100

# fake module
methods_module = ModuleType("<my_methods_module>")


# fill methods to NS class from filesystem 
for cmd, path in cmd_items:
    with open(path) as fp:
        code = compile(fp.read(), path, 'exec')
        #
        print('names in file: {}'.format(code.co_filename))
        print(code.co_names)
        print('-' * 50)
        #
        exec(code, methods_module.__dict__)
        setattr(NS,
                cmd,
                getattr(methods_module, cmd))


# Make instance
inst = NS()

print('\nCalling methods:')

inst_methods = [name for name in dir(inst) if all((not name.startswith('_'),
                                                 callable(getattr(inst,
                                                                  name))))]
for method in inst_methods:
    getattr(inst, method)('Testing text line, epta!')
