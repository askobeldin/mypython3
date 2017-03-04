# -*- coding: utf-8 -*-
############################################################
from zope.interface import Interface
from zope.interface import Attribute
from zope.component import adapts
from zope.component import getGlobalSiteManager
from zope.component import getMultiAdapter
from zope.interface.declarations import implementer


class IAdapteeOne(Interface):
    name = Attribute("""Name of document""")
    body = Attribute("""The document's body""")


class IAdapteeTwo(Interface):
    name = Attribute("""Name of person""")
    age = Attribute("""age of person""")


class IFunctionality(Interface):
    def printData():
        """Printing of data"""


class IFunctionality2(Interface):
    def printData():
        """Printing of data"""


@implementer(IAdapteeOne)
class One(object):
    def __init__(self, name, body):
        self.name, self.body = name, body


@implementer(IAdapteeOne)
class Three(object):
    def __init__(self, name):
        self.name = name
        self.body = u'default body'


@implementer(IAdapteeTwo)
class Two(object):
    def __init__(self, name, age):
        self.name, self.age = name, age


@implementer(IFunctionality)
class MyFunctionality(object):
    adapts(IAdapteeOne, IAdapteeTwo)
    def __init__(self, one, two):
        self.one = one
        self.two = two
    def printData(self):
        print(40 * '=')
        print('Multi adapter')
        print('user: %s\nage: %s' % (self.two.name, self.two.age))
        print('-' * 40)
        print('document\'s name: %s' % self.one.name)
        print('document\'s body: %s' % self.one.body)
        print('\n\n')


@implementer(IFunctionality2)
class MyFunctionality2(object):
    adapts(IAdapteeOne, IAdapteeTwo)
    def __init__(self, one, two):
        self.one = one
        self.two = two
    def printData(self):
        print(10 * '=', 'Multi adapter', 10 * '=')
        print('document\'s name: %s' % self.one.name)
        print('document\'s body: %s' % self.one.body)
        print('user: %s\nage: %s' % (self.two.name, self.two.age))
        print('-' * 10)
        print('\n\n')


if __name__ == '__main__':
    # code here
    gsm = getGlobalSiteManager()
    gsm.registerAdapter(MyFunctionality)
    gsm.registerAdapter(MyFunctionality2)

    one = One('Vedomost', 'blah '*10)
    two = Two('Vasua Pupkin', 33)
    three = Three('Assembly')

    myfunctionality = getMultiAdapter((one, two), IFunctionality)
    myfunctionality.printData()

    myfunctionality = getMultiAdapter((three, two), IFunctionality)
    myfunctionality.printData()

    myfunctionality = getMultiAdapter((one, two), IFunctionality2)
    myfunctionality.printData()

    myfunctionality = getMultiAdapter((three, two), IFunctionality2)
    myfunctionality.printData()
