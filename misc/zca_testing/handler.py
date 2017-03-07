#! /usr/bin/env python
# -*- coding: utf-8 -*-
############################################################
from datetime import datetime
from time import sleep
from textwrap import indent

from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import implementer
from zope.component import getGlobalSiteManager
from zope.component import getMultiAdapter
from zope.component import adapter
from zope.component import handle


class IDocument(Interface):
    summary = Attribute("Document summary")
    body = Attribute("Document text")

@implementer(IDocument)
class Document:
    def __init__(self, summary, body):
        self.summary = summary
        self.body = body

class IDocumentCreated(Interface):
    doc = Attribute('the document that was created')

@implementer(IDocumentCreated)
class DocumentCreated:
    def __init__(self, doc):
        self.doc = doc

@adapter(IDocumentCreated)
def docCreated(event):
    now = datetime.now()
    fmt = '%d.%m.%Y %X.%f'
    event.doc.created = now.strftime(fmt)

@adapter(IDocumentCreated)
def docCreated2(event):
    print('--- Created! -> {} ---'.format(event.doc.summary))

def _attrs(obj):
    return [name for name in dir(obj)
                if not any((name.startswith('_'),
                            callable(name)))]

def print_attrs(obj):
    attrs_list = _attrs(obj)
    values_list = [getattr(obj, name, '--') for name in attrs_list]
    report = zip(attrs_list, values_list)
    for n, v in report:
        print('{}:'.format(n))
        print(indent(v, 4*' '))
    

def main():
    gsm.registerHandler(docCreated)
    gsm.registerHandler(docCreated2)

    documents = (('doc1', Document('a document one', 'Всем привет. Буквально пару слов обо мне.')),
                 ('doc2', Document('a document two', 'Сейчас я переехал в Германию и работаю в InnoGames.')),
                 ('doc3', Document('a document three', 'И сегодня мы поговорим с вами.')))
    # create documents
    for _, d in documents:
        sleep(0.5)
        handle(DocumentCreated(d))

    print('attributes of created documents:')
    for n, d in documents:
        print('Document {!r}'.format(n))
        print_attrs(d)
        print()
        

gsm = getGlobalSiteManager()

if __name__ == '__main__':
    main()
