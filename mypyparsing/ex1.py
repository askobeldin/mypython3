# -*- coding: utf-8 -*-
###############################################################################
from pyparsing import *

identifier = Word(alphas)
print(identifier.parseString("foo"))
print(identifier.parseString("42"))
