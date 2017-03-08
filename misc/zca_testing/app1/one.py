#! /usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
from zope.configuration.config import ConfigurationMachine
from zope.configuration.xmlconfig import registerCommonDirectives
from zope.configuration.xmlconfig import processxmlfile

from zope.component import getGlobalSiteManager

from models import NoseAware, Hobot, Beak
from interfaces import *



thefile = open("configure.zcml")
context = ConfigurationMachine()
registerCommonDirectives(context)
processxmlfile(thefile, context)

gsm = getGlobalSiteManager()
registered = list(gsm.registeredHandlers())
print(registered)


residents = (('Собака', NoseAware(True)),
             ('Лев', NoseAware(False)),
             ('Слон', Hobot(5)),
             ('Ворон', Beak(3, 'черный')),
             ('Воробей', Beak(1, 'коричневый')),
             ('Слоноул', 'fake object here'),
             ('Ворон 2', Beak(5, 'черный')),
             ('Лев 2', NoseAware(False)),
            )


report = '{animal: <10} is soppy nose? {answer: <4}'

print('===== method 1 =====')
for a in residents:
    animal, nose = a
    try:
        answer = INoseAware(nose).isSoppyNose()
    except TypeError as e:
        answer = 'Произошла ошибка при опросе в лесу.'
        pass
    print(report.format(animal=animal, answer=answer))

print('\n===== method 2 =====')
for a in residents:
    animal, nose = a
    if INoseAware.providedBy(nose):
        print(report.format(animal=animal,
                            answer=nose.isSoppyNose()))
    else:
        adapted = queryAdapter(nose, INoseAware)
        if adapted:
            print(report.format(animal=animal,
                                answer=adapted.isSoppyNose()))
        else:
            print(report.format(animal=animal,
                                answer='Нет подходящего адаптера!'))
