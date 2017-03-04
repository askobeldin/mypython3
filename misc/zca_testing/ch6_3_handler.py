#! /usr/bin/env python
# -*- coding: utf-8 -*-
############################################################
from IPython.Shell import IPShellEmbed

from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import implements
from zope.component import adapts
from zope.component import adapter

from zope.component import getGlobalSiteManager

import datetime
import pytz

from zope.component import handle


class IDocument(Interface):
    summary = Attribute("Document summary")
    body = Attribute("Document text")


class Document(object):
    implements(IDocument)

    def __init__(self, summary, body):
        self.summary, self.body = summary, body


class IDocumentCreated(Interface):
    doc = Attribute(u'the document that was created')


class DocumentCreated(object):
    implements(IDocumentCreated)

    def __init__(self, doc):
        self.doc = doc

@adapter(IDocumentCreated)
def documentCreated(event):
    # event.doc.created = datetime.datetime.utcnow()
    msk = pytz.timezone("Europe/Moscow")
    utc = pytz.utc
    fmt = "%d.%m.%Y %H:%M:%S"
    ct = datetime.datetime.now(utc)

    event.doc.created = ct.astimezone(msk).strftime(fmt)


if __name__ == '__main__':
    ipshell = IPShellEmbed()
    # -------------------------
    # code here
    gsm = getGlobalSiteManager()
    gsm.registerHandler(documentCreated)



    doc1 = Document('a\nDocument', 'blah')
    doc2 = Document('a\nDocument', 'blah' * 1000)
    doc3 = Document('a document', 'blah')


    handle(DocumentCreated(doc1))

    # run ipython shell
    ipshell()
