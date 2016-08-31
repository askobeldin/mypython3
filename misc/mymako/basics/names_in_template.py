# -*- coding: utf-8 -*-
#
################################################################################
"""
Try to get names defined in a mako tempate

"""

from mako.template import Template


bar = Template('Basic template with ${name}.')

print('call: bar.render(name=\'...\')')
print(bar.render(name='testing epta'))

#################################################
# how to find identifiers in bar?

from mako import lexer, codegen

lexer = lexer.Lexer(bar.source)
node = lexer.parse()

compiler = lambda: None
compiler.reserved_names = set()

identifiers = codegen._Identifiers(compiler, node)

# All template variables can be found found using this
# object but you are probably interested in the
# undeclared variables:

print('\nIdentifiers in bar template:')
print(identifiers.undeclared)

