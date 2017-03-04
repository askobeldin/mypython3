#! /usr/bin/env python
# -*- coding: utf-8 -*-
############################################################
from zope.interface import Attribute
from zope.interface import Interface
from zope.interface.declarations import implementer

from zope.component.factory import Factory
from zope.component.interfaces import IFactory
from zope.component import getGlobalSiteManager

from zope.component import queryUtility
from zope.component import createObject

# ipython embed shell
from IPython import embed


class IDatabase(Interface):
    def getConnection():
        """Return connection object"""


@implementer(IDatabase)
class FakeDb(object):
    def getConnection(self):
        return "connection"


if __name__ == '__main__':
    # code here
    gsm = getGlobalSiteManager()

    factory = Factory(FakeDb, 'FakeDb')
    gsm.registerUtility(factory, IFactory, 'fakedb')

    a = queryUtility(IFactory, 'fakedb')()

    # run ipython shell
    embed()
