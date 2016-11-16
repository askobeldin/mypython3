# -*- coding: utf-8 -*-
###############################################################################
class Foo:
    def __init__(self):
        self.actions = {}
        self.buffer = []
    def action(self, symbol, func):
        self.actions[symbol] = func

o = Foo()

def func1():
    print('calling func1')

def func2(msg):
    print('calling func2 with {}'.format(msg))

o.action('a', func1)
o.action('b', func2)

o.actions['a']()
o.actions['b']('simple message, epta!')
