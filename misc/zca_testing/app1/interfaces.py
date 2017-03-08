#! /usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
from zope.interface import Interface, Attribute


class INoseAware(Interface):
    soppy = Attribute(u'Мокрый ли нос (boolean)')
    def isSoppyNose():
        """ Метод дает ответ на вопрос о мокроте носа"""

class IHobot(Interface):
    length = Attribute(u'Длина хобота')


class IBeak(Interface):
    length = Attribute('Длина клюва')
    color = Attribute('Цвет клюва')
