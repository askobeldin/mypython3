#! /usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
from zope.interface import Interface, implements
from zope.component import getUtility
from zope.interface import implementer


class IOperation(Interface):
    def __call__(a, b):
        ''' performs operation on two operands '''

@implementer(IOperation)
class Plus(object):
    def __call__(self, a, b):
        return a + b

@implementer(IOperation)
class Minus(object):
    def __call__(self, a, b):
        return a - b

@implementer(IOperation)
class Product(object):
    def __call__(self, a, b):
        return a * b


def myeval(expr):
    a, op, b = expr.split()
    return getUtility(IOperation, op)(float(a), float(b))
