#! /usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
from zope.configuration import xmlconfig
from calc import myeval

xmlconfig.file('configure.zcml')

s1 ='2 + 5'
s2 ='2 * 5'

print(s1, '=',  myeval(s1))
print(s2, '=',  myeval(s2))

