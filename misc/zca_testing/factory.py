#! /usr/bin/env python
# -*- coding: utf-8 -*-
############################################################
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface import implementer

from zope.component import getGlobalSiteManager
from zope.component import queryUtility
from zope.component import createObject

from zope.component.factory import Factory
from zope.component.interfaces import IFactory


class IDatabase(Interface):
    def getConnection():
        """Return connection object"""

@implementer(IDatabase)
class FakeDb(object):
    def getConnection(self):
        return "connection, epta!"

def main():
    # factory = Factory(FakeDb, 'FakeDb')
    factory = Factory(FakeDb)
    gsm.registerUtility(factory, IFactory, 'mydb')

    # print(factory.getInterfaces())
    a = queryUtility(IFactory, 'mydb')()
    print('Connection? -> {}'.format(a.getConnection()))

    # or
    b = createObject('mydb')
    print('Created mydb? -> {}'.format(b.getConnection()))
    

gsm = getGlobalSiteManager()

if __name__ == '__main__':
    main()


