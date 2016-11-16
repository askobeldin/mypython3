# -*- coding: utf-8 -*-
############################################################
"""
variant 2

SM - конечный автомат, разбивает предложение при посимвольном чтении на слова
по пробелам и знакам пунктуации (их игнорирует)

таблица переходов:
((текущее состояние, сигнал), новое состояние)

((R, space), R)
((R, punct), R)
((R, letter), C)
((C, letter), C)
((C, space), R)
((C, punct), R)

"""

import string


SENTENCE = 'this is,a,test,sentence here, ептыть!!!'


isletter = lambda ch: ch.isalnum()
ispunct = lambda ch: ch in string.punctuation

class SM:
    def __init__(self, rules):
        self.cur = ''
        self.buf = []
        self.state = 'R'
        self.container = []
        self.table = {}
        self._inittable(rules)
        # таблица действий при переходе из одного состояния в другое
        self.actions = {
            ('R', 'R'): self._tostate_R,
            ('R', 'C'): self._tostate_C,
            ('C', 'C'): self._tostate_C,
            ('C', 'R'): self._tostate_R_from_C
        }

    def _signal(self, ch):
        if isletter(ch):
            return 'letter'
        if ch.isspace():
            return 'space'
        if ispunct(ch):
            return 'punct'

    def _inittable(self, rules):
        for rule in rules:
            curstate, newstate = rule
            self.table[curstate] = newstate

    def process(self, ch):
        self.cur = ch
        signal = self._signal(ch)
        self.setstate(self.table[self.state, signal])

    def _tostate_C(self):
        # R -> C, C -> C
        self.buf.append(self.cur)
        self.state = 'C'
        return

    def _tostate_R(self):
        # R -> R
        self.cur = ''
        return

    def _tostate_R_from_C(self):
        # C -> R
        self.cur = ''
        self.state = 'R'
        self.container.append(''.join(self.buf))
        self.buf.clear()
        return

    def setstate(self, newstate):
        # call concrete action
        self.actions[self.state, newstate]()

    def aslist(self):
        return self.container



def main(s):
    rules = (
        (('R', 'space'), 'R'),
        (('R', 'punct'), 'R'),
        (('R', 'letter'), 'C'),
        (('C', 'letter'), 'C'),
        (('C', 'space'), 'R'),
        (('C', 'punct'), 'R'),
        )
    a = SM(rules)
    for i in s:
        a.process(i)
    print('{!r} divided on:\n{}'.format(s, a.aslist()))


if __name__ == '__main__':
    main(SENTENCE)

