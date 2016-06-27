# -*- coding: utf-8 -*-
############################################################
def wrap(func):
    def newfunc(*args):
        print('***** newfunc', args)
        return func(*args)
    return newfunc


def cdeco(cls):
    if hasattr(cls, 'do'):
        cls.do = wrap(cls.do)
    if not hasattr(cls, 'foo'):
        cls.foo = 'generated foo attribute'
    return cls

@wrap
def realfunc(*args):
    print('Calling real func', args)

@wrap
def foo(a, b):
    return a * b


@cdeco
class Cls:
    def do(*args):
        print('Cls do', args)


#######################################
realfunc(1, 2, 4)

a = foo(3, 44)
print(a)

c = Cls()
c.do(10, 20)
print(c.foo)
