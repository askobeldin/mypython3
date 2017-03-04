#! /usr/bin/env python
# -*- coding: utf-8 -*-
############################################################
from IPython.Shell import IPShellEmbed

from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import implements
from zope.component import adapts

from zope.component import getGlobalSiteManager


class IValidate(Interface):
    def validate(ob):
        """Determine whether the object is valid Return a string describing a
        validation problem.  An empty string is returned to indicate that the
        object is valid.
        """

class IDocument(Interface):
    summary = Attribute("Document summary")
    body = Attribute("Document text")


class Document(object):
    implements(IDocument)

    def __init__(self, summary, body):
        self.summary, self.body = summary, body

class SingleLineSummary(object):
    adapts(IDocument)
    implements(IValidate)

    def __init__(self, doc):
        self.doc = doc

    def validate(self):
        if '\n' in self.doc.summary:
            return u'Summary sould only have one line'
        else:
            return ''

class AdequateLength(object):
    adapts(IDocument)
    implements(IValidate)

    def __init__(self, doc):
        self.doc = doc

    def validate(self):
        if len(self.doc.body) < 1000:
            return u'too short'
        else:
            return ''



if __name__ == '__main__':
    ipshell = IPShellEmbed()
    # -------------------------
    # code here
    gsm = getGlobalSiteManager()
    gsm.registerSubscriptionAdapter(SingleLineSummary)
    gsm.registerSubscriptionAdapter(AdequateLength)

    from zope.component import subscribers
    doc1 = Document('a\nDocument', 'blah')
    doc2 = Document('a\nDocument', 'blah' * 1000)
    doc3 = Document('a document', 'blah')


    # run ipython shell
    ipshell()
