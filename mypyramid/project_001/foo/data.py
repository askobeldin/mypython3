# -*- coding: utf-8 -*-
#
################################################################################
import foo

class Foo:
    def __init__(self):
        self.a = 'ohuenno!'
        self._show_foo_()
    def _show_foo_(self):
        print('---\nfoo.REG:\n---')
        for e in foo.REG:
            print('{} = {}'.format(e, foo.REG.get(e)))
