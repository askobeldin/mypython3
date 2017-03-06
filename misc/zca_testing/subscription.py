#! /usr/bin/env python
# -*- coding: utf-8 -*-
############################################################
from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import implementer
from zope.component import getGlobalSiteManager
from zope.component import getMultiAdapter
from zope.component import adapter
from zope.component import subscribers

class IValidate(Interface):
    def validate(ob):
        """Determine whether the object is valid Return a string describing a
        validation problem.  An empty string is returned to indicate that the
        object is valid.
        """

class IDocument(Interface):
    summary = Attribute("Document summary")
    body = Attribute("Document text")

@implementer(IDocument)
class Document:
    def __init__(self, summary, body):
        self.summary = summary
        self.body = body

@implementer(IValidate)
@adapter(IDocument)
class SingleLineSummary:
    def __init__(self, doc):
        self.doc = doc
    def validate(self):
        if '\n' in self.doc.summary:
            return 'Summary should only have one line.'
        else:
            return None

@implementer(IValidate)
@adapter(IDocument)
class AdequateLength(object):
    def __init__(self, doc):
        self.doc = doc
    def validate(self):
        if len(self.doc.body) < 500:
            return 'Body too short.'
        else:
            return None


def main():
    gsm.registerSubscriptionAdapter(SingleLineSummary)
    gsm.registerSubscriptionAdapter(AdequateLength)

    docs = (('doc1', Document('a\nsimple Document 1', 'blah')),
            ('doc2', Document('a\nfake Document 2', 'blah' * 1000)),
            ('doc3', Document('a good Document 3', 'blah' * 1000)))
    
    for handle, doc in docs:
        print('Try to validate {}'.format(handle))
        messages = [adapter.validate()
                        for adapter in subscribers([doc], IValidate)
                        if adapter.validate()]
        if messages:
            res = ' '.join(messages)
        else:
            res = 'ok'
        print('Result: {}'.format(res))


gsm = getGlobalSiteManager()


if __name__ == '__main__':
    main()
