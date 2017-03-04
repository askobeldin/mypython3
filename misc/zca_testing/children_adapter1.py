# -*- coding: utf-8 -*-
#
################################################################################
"""
Zope3 Component Architecture: children adapter

Недавно tretiy3 обмолвился, что тем, кто первый раз увидел Zope3 и задает
вопросы на форумах, не хватает простых примеров и разъяснений на пальцах. Сейчас
появился отличный русскоязычный сайт для желающих изучить Zope3 / ZCA (Zope
Component Architecture) - http://zopelada.ru. Там много всяких примеров разной
степени сложности и наглядности. И отличные лекции.

Ну а я сейчас попробую написать совсем "детский", еще более наглядный пример
использования адаптера для приведения одного интерфейса к другому. Наврядли это
здесь нужно кому-то, тем не менее хочу записать его. А получился ли самый
простой в мире пример Zope3 адаптера - судить читателям. Сам пример повторяет
одну из сказок, сочиненных ребенку на ночь, так что прошу не судить строго :)

Итак, представим компонентно-ориентированную систему как разнородное и
несвязанное множество зверюшек в лесу, многие из которых не имеют ничего общего
друг с другом.

Пример приводится в интерактивной сессии Python с доступными для импорта
пакетами zope.interface и zope.component. Регистрация компонент в глобальных
реестрах в условиях сервера приложений делается с помощью ZCML-директив, и это
единственное, для чего они нужны, в действительности. Здесь же регистрировать
будем напрямую, используя zope.component.provideAdapter для глобального
реестра
"""
from zope.interface import Interface, Attribute
from zope.interface import implementer                    
from zope.component import getGlobalSiteManager
from zope.component import adapter
from zope.component import queryAdapter

# Задача - задать каждой зверюшке один и тот же вопрос: "Мокрый ли у тебя
# нос?". Большинство тварей ответят "да" или "нет". Нарисуем общий интерфейс
# для большинства зверюшек:

class INoseAware(Interface):
    soppy = Attribute(u'Мокрый ли нос (boolean)')
    def isSoppyNose():
        """ Метод дает ответ на вопрос о мокроте носа"""

# Реализация интерфейса не имеет значения. Главное, что при приведении к нему
# любого объекта, предоставляющего этот же интерфейс, ошибки не будет.

@implementer(INoseAware)
class NoseAware(object):
    def __init__(self, soppy):
         self.soppy = soppy
    def isSoppyNose(self):
         return self.soppy and u'Да' or u'Нет'

# Это приведение к интерфейсу, и относится к нему в данном случае можно также,
# как к приведению типов (часто встречающемося в коде на Java и других языках со
# статической типизацией.) Правда, в данном случае, "тип" уже тот который нужен
# :)
# Теперь - Слон. У него нет носа, только хобот. (анатомические споры оставим для
# ботаников.) На вопрос "Мокрый ли у тебя нос ?", слон впадает в транс traceback.
# Опишем интерфейс для слона:

class IHobot(Interface):
    length = Attribute(u'Длина хобота')

@implementer(IHobot)
class Hobot(object):
    def __init__(self, length):
        self.length = length

# Реализация интерфейса опять-таки не имеет никакого значения. Ясно, что он не
# имеет ничего общего с INoseAware? и операция вида
# INoseAware(elephant).isSoppyNose()
# (где elephant - экземпляр класса, реализующего интерфейс IHobot?), приведет к
# ошибке.
# Наша задача - сделать "лесной опрос" общим и одинаковым для всех животных.
# Поэтому напишем адаптер интерфейса хоботоносящих млекопитающих к интерфейсу
# носоосведомленных парно- и не-парнокопытных:

@implementer(INoseAware)
@adapter(IHobot)
class HobotToNose(object):
    def __init__(self, context):
        self.context = context
    def isSoppyNose(self):
        return " ".join(
            [u"Нет у меня никакого носа и я не знаю что это такое.",
             u"Зато есть хобот длиной %s метров." % self.context.length])


# Все. Теперь можно посмотреть, что все работает, и при преведении
# объекта-слона к чуждому интерфейсу автоматически отыскивается адаптер
# HobotToNose?:
# Нет у меня никакого носа и я не знаю что это такое.
# Зато есть хобот длиной 5 метров.
# Мда. Чушь какая-то получилась. Но это действительно простой пример адаптера.


# для птиц с клювом

class IBeak(Interface):
    length = Attribute('Длина клюва')
    color = Attribute('Цвет клюва')

@implementer(IBeak)
class Beak:
    def __init__(self, length, color):
        self.length = length
        self.color = color

@implementer(INoseAware)
@adapter(IBeak)
class BeakToNose:
    def __init__(self, context):
        self.context = context
    def isSoppyNose(self):
        return " ".join(['Я птица епта.',
               'У меня клюв - размер: {length:}, цвет: {color:}.'.format(
                             length = self.context.length,
                             color = self.context.color)])


# зарегистрируем их в глобальном сайт-менеджере:
gsm = getGlobalSiteManager()
gsm.registerAdapter(HobotToNose, (IHobot,), INoseAware)
gsm.registerAdapter(BeakToNose, (IBeak,), INoseAware)


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
