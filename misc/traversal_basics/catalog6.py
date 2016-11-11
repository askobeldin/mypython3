#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
################################################################################
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from string import Template
from random import shuffle, randint, choice

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.location import lineage

from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import (resource_path,
                               traverse,
                               find_resource)

from pyramid.decorator import reify



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
        super(SiteFolder, self).__init__(name='',
                                         parent=None,
                                         title=title)


class CatalogDocument(object):
    def __init__(self, name, parent, title, body):
        self.__name__ = name
        self.__parent__ = parent
        self.title = title
        self.body = body


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

        # make catalog db
        self._makeCatalogDB(name='db')

        # attribute for testing
        self['test1'] = randint(100, 1000)

    def __getitem__(self, key):
        print 'Catalog: need key = %s' % key
        try:
            item = super(Catalog, self).__getitem__(key)
            return item
        except KeyError:
            print 'Catalog: key %s error!' % (key,)

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

    def _makeCatalogDB(self, name):
        catdb = CatalogDB(name=name,
                          title='Catalog DB')
        catdb.__parent__ = self
        catdb.db = self.db
        # create node in resource tree
        self[name] = catdb


class CatalogDB(dict):
    def __init__(self, name, title):
        super(CatalogDB, self).__init__()
        self.__name__ = name
        self.title = title

    def __getitem__(self, key):
        print 'Catalog DB: need key = %s' % key
        try:
            db = self.__parent__.db
            # try to get data from database
            data = db.get(key, None)
            if data:
                parentname = data['tag']
                fparent = find_resource(self.__parent__,
                                        parentname)
                item = CatalogDocument(name='%s' % key,
                                         parent=fparent,
                                         title=u'Catalog doc %s' % key,
                                         body=data['data'])
                return item
            else:
                raise KeyError
        except KeyError:
            print 'Catalog DB: key %s error!' % (key,)




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
                 $test1
                 <hr>
                 <p>Tags: $keys</p>
                 </body>
                 </html>
                 """)
    # try to find resource `test1` in context
    res1 = find_resource(context, 'test1')
    t_test1 = res1 if res1 else ''
    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title,
                               test1 = '<p>test1 = %s</p>' % t_test1,
                               keys = getCatalogTags(request))
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
                 <h3>Links:</h3>
                 $keys
                 </body>
                 </html>
                 """)
    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title,
                               keys = mkCatalogFolderLinks(request))
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')

def view_catalogdb(context, request):
    s = Template("""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Catalog DB: $name</title>
                 </head>
                 <body>
                 <p>BC: $breadcrumbs</p>
                 <hr>
                 <h3>title: $title</h3>
                 <hr>
                 <p>This is an internal database page</p>
                 <h3>Actions:</h3>
                 <ul>
                     <li><a href="$addlink">ADD</a></li>
                 </ul>
                 <h3>Last 3 items:</h3>
                 $lastdbitems
                 </body>
                 </html>
                 """)
    # make link for `add` view
    addlink = request.resource_url(context, '@@add')

    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title,
                               lastdbitems = mkLastDBLinks(request),
                               addlink = addlink)
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')

def view_catalogdb_add(context, request):
    if request.method == 'POST':
        # handle forms data
        fitem = request.POST.get('item', None)
        if fitem:
            print 'ADD to DB: %s' % fitem
            # create new record in db with random tag
            catalog = context.__parent__
            db = catalog.db
            tags = catalog.tags

            newindex = int(max(db, key=int)) + 1
            newtag = choice(tags)
            db[str(newindex)] = {'data': fitem,
                                 'tag': newtag}
            # update subfolder for newtag
            catalog[newtag].updateDocuments()
            # redirect to created item
            newurl = resource_path(catalog, 'db', str(newindex))
            return HTTPFound(newurl)
        else:
            # sent not filled form
            s = Template("""
                         <!DOCTYPE html>
                         <html>
                         <head>
                         <title>Adding to catalog DB: $name</title>
                         </head>
                         <body>
                         <p>BC: $breadcrumbs</p>
                         <hr>
                         <h1>You should write text!</h1>
                         </body>
                         </html>
                         """)
            output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                                       name = context.__name__)
    else:
        # method GET - return form
        s = Template("""
                     <!DOCTYPE html>
                     <html>
                     <head>
                     <title>Adding to catalog DB: $name</title>
                     </head>
                     <body>
                     <p>BC: $breadcrumbs</p>
                     <hr>
                     <h3>Adding to: $title</h3>
                     <hr>
                     <p>Add item for catalog DB</p>
                     <form action="" method="post">
                         <input type="text" maxlength="200" name="item">
                         <input type="submit" value="ADD">
                     </form>
                     </body>
                     </html>
                     """)
        output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                                   name = context.__name__,
                                   title = context.title)

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


def getCatalogTags(request):
    leaves = request.context.tags
    obj = request.context

    li = ['<li>'  + '<a href="' + request.resource_url(obj[i]) + '">' + i +
          '</a></li>' for i in leaves]
    return "<ul>" + "\n".join(li) + "</ul>"


def mkCatalogFolderLinks(request):
    leaves = request.context.documents
    catalog = request.context.__parent__
    catdb = find_resource(catalog, 'db')

    li = ['<li>'  + '<a href="' + request.resource_url(catdb, i) + '">' + i +
          '</a></li>' for i in leaves]
    return "<ul>" + "\n".join(li) + "</ul>"


def mkLastDBLinks(request):
    catdb = request.context
    db = request.context.__parent__.db
    dbkeys = db.keys()
    dbkeys.sort(key=int,
                reverse=True)
    # last 3 items in db
    leaves = dbkeys[:3]

    li = ['<li>'  + '<a href="' + request.resource_url(catdb, i) + '">' + i +
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
RTREE = SiteFolder(u'Test catalog 4')




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

DATA['11'] = {'data': 'this is a test data 011', 'tag': 'first'}
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

    config.add_view(view=view_catalogdb,
                    context=CatalogDB)

    config.add_view(view=view_catalogdb_add,
                    name='add',
                    context=CatalogDB)

    config.add_view(view=view_catalogdocument,
                    context=CatalogDocument)


    # make resources tree
    makeResourcesTree()

    # create my catalog
    RTREE['cat'] = Catalog(name='cat',
                           parent=RTREE,
                           title='Catalog',
                           db=DATA)

    # RTREE['cat2'] = Catalog(name='cat2',
                           # parent=RTREE,
                           # title='Catalog',
                           # db=DATA)

    # ----------------------------------------------------
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
