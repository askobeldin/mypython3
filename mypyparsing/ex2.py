# -*- coding: utf-8 -*-
###############################################################################
from pyparsing import Word, alphas


greet = Word( alphas ) + "," + Word( alphas ) + "!" # <-- grammar defined here
greet2 = Word( alphas ) + "," + Word( alphas )      # <-- grammar defined here

hello = "Hello, World!"

print (hello, "->", greet.parseString(hello))
print (hello, "->", greet2.parseString(hello))
