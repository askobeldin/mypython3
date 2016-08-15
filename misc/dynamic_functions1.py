# -*- coding: utf-8 -*-
#
################################################################################
"""
Попытка поэкспериментировать с динамическим созданием функций и декораторами

ерунда пока что получается

"""

import pprint
import types
from weakref import WeakKeyDictionary, WeakValueDictionary


"""
Template is


def register(tag):
    def decorate(func):
        return func
    return decorate

"""

# REGISTRY = {}
# REGISTRY = WeakKeyDictionary()
REGISTRY = WeakValueDictionary()


def register(tag):
    def decorate(func):
        _f = types.FunctionType(func.__code__, globals())
        REGISTRY[tag] = _f
        # print('type(func) is {}'.format(type(func)))
        # del globals()[func.__name__]
        # del func.__qualname__
        return _f
    return decorate



@register(tag='a')
def f1():
    print('This is f1 call')

@register(tag='b')
def f2():
    print('This is f2 call')


def main():
    f1()
    f2()
    print('Registry is:\n{}'.format(REGISTRY))
    print('\nGlobals is:')
    pprint.pprint(globals())


if __name__ == '__main__':
    main()
