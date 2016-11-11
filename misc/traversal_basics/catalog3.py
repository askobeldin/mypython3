#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
################################################################################
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from string import Template
from random import shuffle

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.location import lineage

from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import (resource_path,
                               traverse,
                               find_resource)

from pyramid.decorator import reify

"""
from pyramid.httpexceptions import HTTPFound

#################################
# make a new Document
#
title = appstruct['title']
body = appstruct['body']
name = str(randint(0, 999999))
new_document = Document(name, self.context, title, body)
self.context[name] = new_document

######################################
# Redirect to the new document
#
url = self.request.resource_url(new_document)
return HTTPFound(location=url)
"""

class Folder(OrderedDict):
    def __init__(self, name, parent, title):
        super(Folder, self).__init__()
        self.__name__ = name
        self.__parent__ = parent
        self.title = title


class Document(object):
    def __init__(self, name, parent, title, body):
        self.__name__ = name
        self.__parent__ = parent
        self.title = title
        self.body = body


class SiteFolder(Folder):
    def __init__(self, title):
        super(Folder, self).__init__()
        self.__name__ = ''
        self.__parent__ = None
        self.title = title


class CatalogDocument(object):
    def __init__(self, name, parent, title, body):
        self.__name__ = name
        self.__parent__ = parent
        self.title = title
        self.body = body

    # try to override resources path
    # def __resource_url__(self, request, info):
        # print '### Call __resource_url__ ###'
        # return info['app_url'] + info['virtual_path']


# subfolder for catalog
class CatalogFolder(OrderedDict):
    def __init__(self, name, parent, title):
        super(CatalogFolder, self).__init__()
        self.__name__ = name
        self.__parent__ = parent
        self.title = title

        # subfolder keys items from database
        self.documents = []
        self.documents = self._initDocuments()

        # make documents in subfolder by tag
        self._makeCatalogFolderDocs()

    def __getitem__(self, key):
        print 'CatalogFolder: need key = %s' % key
        try:
            item = super(CatalogFolder, self).__getitem__(key)
        except KeyError:
            print 'CatalogFolder: key %s error!' % (key,)
        return item

    def __setitem__(self, key, value):
        print 'CatalogFolder: save key = %s' % key
        try:
            super(CatalogFolder, self).__setitem__(key, value)
        except KeyError:
            print 'CatalogFolder: save key %s error!' % (key,)

    def updateDocuments(self):
        self.documents = self._initDocuments()

    def _initDocuments(self):
        thistag = self.__name__
        docs = [k for k,v in self.__parent__.db.items()
                if v['tag'] == thistag]
        docs.sort(key=int)
        return docs

    def _makeCatalogFolderDocs(self):
        if self.documents:
            for doc in self.documents:
                self[doc] = CatalogDocument(name=doc,
                                     parent=self,
                                     title=u'Catalog doc %s' % doc,
                                     body=self.__parent__.db[doc]['data'])

    # def _makeCatalogFolderLinks(self):
        # if self.documents:
            # for doc in self.documents:
                # self[doc] = CatalogDocument(name=doc,
                                     # parent=self,
                                     # title=u'Catalog doc %s' % doc,
                                     # body=self.__parent__.db[doc]['data'])


class Catalog(OrderedDict):
    def __init__(self, name, parent, title, db):
        super(Catalog, self).__init__()
        self.__name__ = name
        self.__parent__ = parent
        self.title = title
        self.db = db

        # tag list
        self.tags = []
        self.tags = self._loadTagsList()

        # make subfolders
        self._makeSubfolders()

    def __getitem__(self, key):
        print 'Catalog: need key = %s' % key
        try:
            item = super(Catalog, self).__getitem__(key)
        except KeyError:
            print 'Catalog: key %s error!' % (key,)
        return item

    def __setitem__(self, key, value):
        print 'Catalog: save key = %s' % key
        try:
            super(Catalog, self).__setitem__(key, value)
        except KeyError:
            print 'Catalog: save key %s error!' % (key,)

    def updateTagsList(self):
        self.tags = self._loadTagsList()


    def _loadTagsList(self):
        s = set()
        for k, v in self.db.items():
            s.add(v['tag'])
        lst = list(s)
        lst.sort()
        return lst

    def _makeSubfolders(self):
        # make catalog subfolders from tags 
        if self.tags:
            for tag in self.tags:
                self[tag] = CatalogFolder(name=tag,
                                   parent=self,
                                   title=u'Subfolder %s' % tag)



###############################################################################
# views
#
#
def view_site(context, request):
    s = Template("""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Site: $title</title>
                 </head>
                 <body>
                 <p>Leaves: $keys</p>
                 </body>
                 </html>
                 """)
    output = s.safe_substitute(title = context.title,
                               keys = getFolderLeaves(request))
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')


def view_folder(context, request):
    s = Template("""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Folder $name</title>
                 </head>
                 <body>
                 <p>BC: $breadcrumbs</p>
                 <hr>
                 <h3>title: $title</h3>
                 <hr>
                 <p>Leaves: $keys</p>
                 </body>
                 </html>
                 """)
    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title,
                               keys = getFolderLeaves(request))
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')


def view_doc(context, request):
    s = Template("""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Document $name</title>
                 </head>
                 <body>
                 <p>BC: $breadcrumbs</p>
                 <hr>
                 <h3>Title: $title</h3>
                 <p>Body: $body</p>
                 <hr>
                 </body>
                 </html>
                 """)
    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title,
                               body = context.body)
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')


def view_catalog(context, request):
    s = Template("""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Catalog $name</title>
                 </head>
                 <body>
                 <p>BC: $breadcrumbs</p>
                 <hr>
                 <h3>title: $title</h3>
                 <hr>
                 <p>Leaves: $keys</p>
                 </body>
                 </html>
                 """)
    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title,
                               keys = getFolderLeaves(request))
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')


def view_catalogfolder(context, request):
    s = Template("""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Catalog subfolder $name</title>
                 </head>
                 <body>
                 <p>BC: $breadcrumbs</p>
                 <hr>
                 <h3>title: $title</h3>
                 <hr>
                 <p>Leaves: $keys</p>
                 </body>
                 </html>
                 """)
    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title,
                               keys = getFolderLeaves(request))
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')


def view_catalogdocument(context, request):
    s = Template("""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Catalog document $name</title>
                 </head>
                 <body>
                 <p>BC: $breadcrumbs</p>
                 <hr>
                 <h3>Title: $title</h3>
                 <p>Body: $body</p>
                 <hr>
                 </body>
                 </html>
                 """)
    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title,
                               body = context.body)
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')



###############################################################################
# functions
#
def getBreadCrumbs(request):
    cr = [(request.resource_url(i), i.title) for i in lineage(request.context)]
    cr.reverse()
    li = ['<li>' + '<a href="' + i[0] + '">' + i[1] + '</a></li>'
          for i in cr[:-1]]
    #last item of breadcrumbs
    li.append('<li>' + cr[-1][1] + '</li>')
    return "<ul>" + "\n".join(li) + "</ul>"


def getFolderLeaves(request):
    leaves = request.context.items()
    li = ['<li>'  + '<a href="' + request.resource_url(i[1]) + '">' + i[0] +
          '</a></li>' for i in leaves]
    return "<ul>" + "\n".join(li) + "</ul>"


def mkHTMLfromList(lst):
    li = ['<li>' + unicode(item) + '</li>' for item in lst]
    return "<ul>" + "\n".join(li) + "</ul>"





def makeResourcesTree():
    folder1 = RTREE['f1'] = Folder('f1', RTREE, u'Folder one')
    folder2 = RTREE['f2'] = Folder('f2', RTREE, u'Folder two')

    d1 = folder1['d1'] = Document(name='d1',
                                  parent=folder1,
                                  title=u'Testing document 1',
                                  body=u'Body of testing document 1')

    d2 = folder1['d2'] = Document(name='d2',
                                  parent=folder1,
                                  title=u'Testing document 2',
                                  body=u'Body of testing document 2')

    # generating some docs in folder 2
    for i in xrange(1, 6):
        name = 'd%s' % i
        folder2[name] = Document(name=name,
                                 parent=folder2,
                                 title=u'Generated document %s' % name,
                                 body=u'Generated body of document %s' % name)



def get_root(request):
    return RTREE




###############################################################################
# Resources tree
#
RTREE = SiteFolder(u'Test catalog1')




###############################################################################
# Data
#
DATA = {}
DATA['1'] = {'data': 'this is a test data 1', 'tag': 'third'}
DATA['2'] = {'data': 'this is a test data 2', 'tag': 'first'}
DATA['3'] = {'data': 'this is a test data 3', 'tag': 'second'}
DATA['4'] = {'data': 'this is a test data 4', 'tag': 'first'}
DATA['5'] = {'data': 'this is a test data 5', 'tag': 'first'}
DATA['6'] = {'data': 'this is a test data 6', 'tag': 'second'}
DATA['7'] = {'data': 'this is a test data 7', 'tag': 'first'}
DATA['8'] = {'data': 'this is a test data 8', 'tag': 'second'}
DATA['9'] = {'data': 'this is a test data 9', 'tag': 'third'}
DATA['10'] = {'data': 'this is a test data 10', 'tag': 'second'}

DATA['11'] = {'data': 'this is a test data 11', 'tag': 'first'}
DATA['12'] = {'data': 'this is a test data 12', 'tag': 'second'}
DATA['13'] = {'data': 'this is a test data 13', 'tag': 'third'}
DATA['14'] = {'data': 'this is a test data 14', 'tag': 'first'}
DATA['15'] = {'data': 'this is a test data 15', 'tag': 'first'}
DATA['16'] = {'data': 'this is a test data 16', 'tag': 'third'}
DATA['17'] = {'data': 'this is a test data 17', 'tag': 'first'}
DATA['18'] = {'data': 'this is a test data 18', 'tag': 'third'}
DATA['19'] = {'data': 'this is a test data 19', 'tag': 'first'}
DATA['20'] = {'data': 'this is a test data 20', 'tag': 'first'}


###############################################################################
# main
#
#
if __name__ == '__main__':

    config = Configurator(root_factory=get_root)

    config.add_view(view=view_site,
                    context=SiteFolder)

    config.add_view(view=view_folder,
                    context=Folder)

    config.add_view(view=view_doc,
                    context=Document)

    config.add_view(view=view_catalog,
                    context=Catalog)

    config.add_view(view=view_catalogfolder,
                    context=CatalogFolder)

    config.add_view(view=view_catalogdocument,
                    context=CatalogDocument)


    # make resources tree
    makeResourcesTree()

    # create my catalog
    RTREE['cat'] = Catalog(name='cat',
                           parent=RTREE,
                           title='Catalog',
                           db=DATA)






    # ----------------------------------------------------
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
