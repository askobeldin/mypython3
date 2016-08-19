# -*- coding: utf-8 -*-
#
################################################################################

# эксперименты с классами, eval, exec и пр.

from collections import deque
import string

################################################
# class foo:
    # def one(self):
        # print('one')
    # def two(self):
        # print('two')
    # def three(self):
        # print('three')

# a = foo()

# dd = dict(vars(foo))

# dd['one'](a) --> call a.one()
################################################

# конечный автомат, обрабатывающий последовательность символов:
# - при поступлении на его вход буквы - кладет ее в буфер:
    # - если "#" - то система ожидает следующего символа:
        # - если буква - добавляет в буфер 2 этих буквы
        # - если цифра - добавляет в буфер последнюю букву цифра раз
# - при поступлении цифры - выталкивает накопленный буфер в виде строки букв, а
#   цифру игнорирует; если буфер пуст - просто игнорирует цифру
# при окончании последовательности - выталкивает буфер с добавленным последним символом
#
# state = (ready, collect, waiting)
# waiting - after `#`
#

def examine(symbol):
    if any((symbol.isalpha(), symbol.isspace())):
        return 'letter'
    if symbol.isdecimal():
        return 'number'
    if symbol in '#':
        return 'hashmark'


class StateMachine:
    def __init__(self, table):
        self.statetable = table
        self.lastitem = ''
        self.state = 'ready'
        self.currentitem = None
        self.buffer = deque()
    def process(self, textline):
        for symbol in textline:
            self.currentitem = symbol
            print('{!r}'.format(examine(symbol)))


###########################################################
# table of jumps
#
# ((state, letter), 'macroprogramm')
#
TABLE = {
    ('ready', 'letter'): 'add',
    ('collect', 'letter'): 'add',
    ('waiting', 'letter'): 'add; add',

    ('ready', 'number'): 'skip',
    ('collect', 'number'): 'pop',
    ('waiting', 'number'): 'addn',

    ('ready', 'hashmark'): 'wait',
    ('collect', 'hashmark'): 'wait',
    ('waiting', 'hashmark'): 'wait',
}


# s = 'test make7me# let8solid#7# creo'
s = 'test3make7me'


# main
a = StateMachine(TABLE)
a.process(s)
