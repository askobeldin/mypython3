# -*- coding: utf-8 -*-
############################################################
from zope.interface import Interface
from zope.interface import Attribute
from zope.interface import implementer
from zope.component import getGlobalSiteManager
from zope.component import getMultiAdapter
from zope.component import adapter


class IDocument(Interface):
    name = Attribute("""Name of document""")
    body = Attribute("""The document's body""")

class ISimpleView(Interface):
    """Simple plain text view of document
    """
    doc = Attribute('Simple view')

class IFileView(Interface):
    """View of document for file
    """
    doc = Attribute('File view')
    filename = Attribute('Name of the file')
    
class IPrinter(Interface):
    """Prints data to the screen
    """
    def printData():
        """Printing of data"""

@implementer(IDocument)
class Document:
    def __init__(self, name, body):
        self.name = name
        self.body = body

@implementer(ISimpleView)
class SimpleView:
    def __init__(self, document):
        n = document.name
        b = document.body
        line = len(n) * '=' 
        self.doc = '\n'.join((n, line, b))

@implementer(IPrinter)
@adapter(IDocument, ISimpleView)
class SimplePrinter:
    def __init__(self, doc, view):
        self.doc = doc
        self.view = view
    def printData(self):
        view = self.view.doc
        print('{}'.format(view))

@implementer(IFileView)
class FileView:
    def __init__(self, document, filename):
        n = document.name
        b = document.body
        line = len(n) * '#' 
        self.doc = '\n'.join((line, n, line, 'body:', b, line))
        self.filename = filename

@implementer(IPrinter)
@adapter(IDocument, IFileView)
class SimpleFilePrinter:
    def __init__(self, doc, view):
        self.doc = doc
        self.view = view
    def printData(self):
        view = self.view.doc
        print('Как бы вывод в файл: {}'.format(self.view.filename))
        print('{}'.format(view))
        
def main():
    d = Document(name="Ведомость покупных изделий",
                 body='\n'.join(
                     ('Строка один',
                      'Строка два',
                      'Строка три, епта',)))
    v = SimpleView(d)
    m = getMultiAdapter((d, v), IPrinter)
    m.printData()

    print('\n'*2)

    fv = FileView(d, '/home/filename.txt')
    m2 = getMultiAdapter((d, fv), IPrinter)
    m2.printData()


gsm = getGlobalSiteManager()
gsm.registerAdapter(SimplePrinter)
gsm.registerAdapter(SimpleFilePrinter)

if __name__ == '__main__':
    main()
