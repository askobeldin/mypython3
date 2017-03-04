#! /usr/bin/env python
# -*- coding: utf-8 -*-
############################################################
from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import implements
from zope.component import adapts

from zope.component import getGlobalSiteManager
from zope.component import getMultiAdapter


class IDocument(Interface):
    name = Attribute("""Name of document""")
    body = Attribute("""The document's body""")


class IView(Interface):
    def printViewData():
        """Printing view"""


class IFunctionality(Interface):
    def printData():
        """Printing of data"""


class Document(object):
    implements(IDocument)

    def __init__(self, name, body):
        self.name, self.body = name, body


class View(object):
    implements(IView)

    def printViewData(self, data):
        print '--- %s' % data


class View2(object):
    implements(IView)

    def printViewData(self, data):
        print 'view2 ***** %s' % data


class MyFunctionality(object):
    implements(IFunctionality)

    adapts(IDocument, IView)

    def __init__(self, doc, view):
        self.doc = doc
        self.view = view

    def printData(self):
        self.view.printViewData(self.doc.name)
        self.view.printViewData(self.doc.body)


if __name__ == '__main__':
    # code here
    gsm = getGlobalSiteManager()
    gsm.registerAdapter(MyFunctionality)

    doc = Document('Vedomost', 'blah '*10)
    view1 = View()
    view2 = View2()

    m1 = getMultiAdapter((doc, view1), IFunctionality)
    m2 = getMultiAdapter((doc, view2), IFunctionality)

    for v in (m1, m2):
        v.printData()
