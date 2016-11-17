#! /usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
"""
variant 3

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


isletter = lambda ch: ch.isalnum()
ispunct = lambda ch: ch in string.punctuation
isspace = lambda ch: ch.isspace()


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


# state machine
class SM:
    def __init__(self, table):
        self.cur = ''
        self.buf = []
        self.state = 'R'
        self.container = []
        self.table = {}
        self.symrules = None
        self._inittable(table)
        # таблица действий при переходе из одного состояния в другое
        self.actions = {}

    def _inittable(self, table):
        for rule in table:
            curstate, newstate = rule
            self.table[curstate] = newstate

    def _signal(self, ch):
        for f, sym in self.symrules:
            if f(ch):
                return sym

    def process(self, ch):
        self.cur = ch
        signal = self._signal(ch)
        self.setstate(self.table[self.state, signal])

    def setstate(self, newstate):
        # call concrete action
        self.actions[self.state, newstate](self)

    def aslist(self):
        return self.container


def main():
    # text to processing
    SENTENCE = 'this\t\t is,a,test,sentence\n here, ептыть!!!'

    # кортеж функций и соответствующих им символов
    # автомат вызывает их при тестировании входного символа по порядку
    symbol_rules = ((isletter, 'letter'),
                    (ispunct, 'punct'),
                    (isspace, 'space'))

    # таблица переходов автомата
    # (((current state, symbol), next state), ... )
    transition_table = (
        (('R', 'space'), 'R'),
        (('R', 'punct'), 'R'),
        (('R', 'letter'), 'C'),
        (('C', 'letter'), 'C'),
        (('C', 'space'), 'R'),
        (('C', 'punct'), 'R'),
    )

    # таблица функций вызываемых автоматом при переходе из одного состояния в
    # другое
    actions = {
                ('R', 'R'): _tostate_R,
                ('R', 'C'): _tostate_C,
                ('C', 'C'): _tostate_C,
                ('C', 'R'): _tostate_R_from_C
    }

    # instance of state machine
    a = SM(transition_table)
    # configure machine
    a.symrules = symbol_rules
    a.actions = actions

    # processing sentence thru SM
    for i in SENTENCE:
        a.process(i)
    print('Processing: {!r}\nResult: {}'.format(SENTENCE, a.aslist()))


if __name__ == '__main__':
    main()

