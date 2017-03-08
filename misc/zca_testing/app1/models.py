#! /usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################

class NoseAware:
    def __init__(self, soppy):
         self.soppy = soppy
    def isSoppyNose(self):
         return self.soppy and u'Да' or u'Нет'


class Hobot:
    def __init__(self, length):
        self.length = length


class Beak:
    def __init__(self, length, color):
        self.length = length
        self.color = color


class HobotToNose:
    def __init__(self, context):
        self.context = context
    def isSoppyNose(self):
        return " ".join(
            [u"Нет у меня никакого носа и я не знаю что это такое.",
             u"Зато есть хобот длиной %s метров." % self.context.length])

class BeakToNose:
    def __init__(self, context):
        self.context = context
    def isSoppyNose(self):
        return " ".join(['Я птица епта.',
               'У меня клюв - размер: {length:}, цвет: {color:}.'.format(
                             length = self.context.length,
                             color = self.context.color)])



