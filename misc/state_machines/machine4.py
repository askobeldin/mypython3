# -*- coding: utf-8 -*-
###############################################################################
"""
variant 4

SM - конечный автомат, разбивает предложение при посимвольном чтении на слова
по пробелам и знакам пунктуации (их игнорирует)

таблица переходов:
    (`текущее состояние`, `сигнал`, `новое состояние`)
    (`текущее состояние`, '*', `новое состояние`)       TODO: не реализовано
или
    (`текущее состояние`, (`сигнал1`, `сигнал2`, ...), `новое состояние`)

R - ready, C - collecting
* - произвольный сигнал

"""
import string
from enum import Enum
from collections.abc import Iterable


isletter = lambda ch: ch.isalnum()
ispunct = lambda ch: ch in string.punctuation
isspace = lambda ch: ch.isspace()

# possible signals
s = Enum('s', ['space', 'punct', 'letter'], module=__name__)

# possible states of machine
st = Enum('st', ['R', 'C'], module=__name__)

def _tostate_C(self):
    # R -> C, C -> C
    self.buf.append(self.cur)
    self.state = st.C
    return

def _tostate_R(self):
    # R -> R
    self.cur = ''
    return

def _tostate_R_from_C(self):
    # C -> R
    self.cur = ''
    self.state = st.R
    self.container.append(''.join(self.buf))
    self.buf.clear()
    return

# state machine
class SM:
    def __init__(self, table):
        self.cur = ''
        self.buf = []
        self.state = st.R
        self.container = []
        self.table = {}
        self.symrules = None
        self._inittable(table)
        # таблица действий при переходе из одного состояния в другое
        self.actions = {}

    def _inittable(self, table):
        for rule in table:
            curstate, signals, newstate = rule
            if isinstance(signals, Iterable):
                for signal in signals:
                    self.table[curstate, signal] = newstate
            else:
                self.table[curstate, signals] = newstate


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
    symbol_rules = ((isletter, s.letter),
                    (ispunct, s.punct),
                    (isspace, s.space))

    # таблица переходов автомата
    # ((current state, symbols, next state), ... )
    transition_table = (
        (st.R, (s.space, s.punct), st.R),
        (st.R, s.letter, st.C),
        (st.C, s.letter, st.C),
        (st.C, (s.space, s.punct), st.R),
    )

    # таблица функций вызываемых автоматом при переходе из одного состояния в
    # другое
    actions = {
        (st.R, st.R): _tostate_R,
        (st.R, st.C): _tostate_C,
        (st.C, st.C): _tostate_C,
        (st.C, st.R): _tostate_R_from_C
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
