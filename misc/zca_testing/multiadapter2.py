#! /usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
from textwrap import indent
from zope.interface import (Interface,
                            Attribute,
                            implementer)
from zope.component import (adapter,
                            getGlobalSiteManager,
                            getMultiAdapter)


class IDocument(Interface):
    name = Attribute("""Name of document""")
    body = Attribute("""The document's body""")

class IView(Interface):
    """view
    """
    def printViewData():
        """Printing view"""

class IFunctionality(Interface):
    def printData():
        """Printing of data"""


@implementer(IDocument)
class Document:
    def __init__(self, name, body):
        self.name = name
        self.body = body

@implementer(IView)
class View:
    def _attrs(self, obj):
        return [name for name in dir(obj)
                    if not any((name.startswith('_'),
                               callable(name)))]
    def printViewData(self, data):
        attrs_list = self._attrs(data)
        values_list = [getattr(data, name, '--') for name in attrs_list]
        report = zip(attrs_list, values_list)
        print('===== view =====')
        for n, v in report:
            print('{}:'.format(n))
            print(indent(v, 4*' '))
        print('----- end of view -----')

@implementer(IView)
class View2:
    def printViewData(self, data):
        report = 'view2 > {}'
        print(report.format(data.name))
        print(report.format(data.body))

@implementer(IFunctionality)
@adapter(IDocument, IView)
class MyFunctionality:
    def __init__(self, doc, view):
        self.doc = doc
        self.view = view
    def printData(self):
        self.view.printViewData(self.doc)


def main():
    """main function
    """
    doc = Document('Vedomost', 'blah '*10)

    view1 = View()
    view2 = View2()

    m1 = getMultiAdapter((doc, view1), IFunctionality)
    m2 = getMultiAdapter((doc, view2), IFunctionality)

    for v in (m1, m2):
        v.printData()


gsm = getGlobalSiteManager()
gsm.registerAdapter(MyFunctionality)


if __name__ == '__main__':
    main()
