#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
################################################################################
from string import Template
import collections
import os.path
import sqlite3
from sys import exit

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.location import lineage

from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import (resource_path,
                               traverse,
                               find_resource)
from pyramid.decorator import reify

#######################################
# configs
#
DEBUG = True

dbfilename = os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'library.db'))


class MyContainer(collections.MutableMapping):
    __parent__ = __name__ = None

    def __init__(self):
        self.ckeys = collections.deque()
        self.container = {}

    def __getitem__(self, key):
        if DEBUG:
            print '%s(%s): call __getitem__, key = %s' % (self.__class__.__name__,
                                                    getattr(self, 'title', 'XXX'),
                                                     key)
        try:
            item = self.container[key]
            return item
        except KeyError as e:
            raise

    def __setitem__(self, key, value):
        if key in self.ckeys:
            self.container[key] = value
        else:
            self.ckeys.append(key)
            self.container[key] = value
        value.__name__ = key
        value.__parent__ = self
        if DEBUG:
            print '%s(%s): call __setitem__, key = %s' % (self.__class__.__name__,
                                                    getattr(self, 'title', 'XXX'),
                                                     key)

    def __delitem__(self, key):
        if key in self.ckeys:
            self.ckeys.remove(key)
            del self.container[key]
        else:
            raise KeyError

    def __len__(self):
        return len(self.ckeys)

    def __iter__(self):
        return iter(self.ckeys)


class Folder(MyContainer):
    def __init__(self, title):
        super(Folder, self).__init__()
        self.title = title


class Document(object):
    __parent__ = __name__ = None
    def __init__(self, title, description, body):
        self.title = title
        self.description = description
        self.body = body


class SiteFolder(Folder):
    pass


class LibCategory(MyContainer):
    def __init__(self, data):
        super(LibCategory, self).__init__()
        self.title = data['title']
        self.id = data['id']
        self.href = data['href']


class Library(MyContainer):
    def __init__(self, title, db):
        super(Library, self).__init__()
        self.title = title
        if os.path.exists(db):
            self.dbname = db
        else:
            print "Can\'t find database %s\n" % db
            exit(1)
        # init categories containers from db
        self._make_categories_from_db()

    def _make_categories_from_db(self):
        with sqlite3.connect(self.dbname,
                detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("""SELECT id, title, href FROM categories""")
            rows = cur.fetchall()
            data = [{'id': i['id'],
                     'title': i['title'],
                     'href': i['href']} for i in rows]
            # sorting
            data = sorted(data,
                          cmp=lambda x, y: cmp(x.lower(), y.lower()),
                          key=lambda x: x['title'])
            # make categories
            for item in data:
                self[item['href']] = LibCategory(item)


############################################################
# functions
#
def get_root(request):
    return RTREE


def getBreadCrumbs(request):
    cr = [(request.resource_url(i), i.title)
          for i in lineage(request.context)]
    cr.reverse()
    li = ['<li>' + '<a href="' + i[0] + '">' +
          i[1] + '</a></li>' for i in cr[:-1]]
    #last item of breadcrumbs
    li.append('<li>' + cr[-1][1] + '</li>')
    return "<ul>" + "\n".join(li) + "</ul>"


def getFolderLeaves(request):
    leaves = [(request.resource_url(v), v.title)
          for k, v in request.context.items()]
    li = ['<li>' + '<a href="' + i[0] + '">' +
          i[1] + '</a></li>' for i in leaves]
    return "<ul>" + "\n".join(li) + "</ul>"


def make_table_books(data):
    """
    Make html table from data. Return string.
    """
    tbl1 = [u'<table cellspacing="2" border="1" cellpadding="5" width="100%"><thead><tr>',
           u'<th width="60%">Наименование</th>',
           u'<th>Автор</th>',
           u'<th>Издательство</th>',
           u'<th>Издана</th>',
           u'</tr></thead><tbody>']

    tbl2 = [u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' %
            (i['title'], i['author'], i['publisher'], i['year']) for i in data]

    tbl3 = [u'</tbody>', '</table>']
    return u''.join(tbl1 + tbl2 + tbl3)


############################################################
# views
#
def view_site(context, request):
    s = Template(u"""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>$title</title>
                 </head>
                 <body>
                 <h1>Main page of site $title</h1>
                 <p>Leaves:</p>$keys
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
    s = Template(u"""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Folder $name</title>
                 </head>
                 <body>
                 <p>BC:</p>$breadcrumbs
                 <hr>
                 <h3>title: $title</h3>
                 <hr>
                 <p>Leaves:</p>$keys
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

############
# XXX
# def view_folder(context, request):

    # return Response(body=u'Testing view for folder',
                   # charset='utf-8',
                   # content_type='text/html',
                   # content_language='ru')


def view_doc(context, request):
    s = Template(u"""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Document $name</title>
                 </head>
                 <body>
                 <p>BC:</p>$breadcrumbs
                 <hr>
                 <h3>$title</h3>
                 <em>$description</em>
                 $body
                 <hr>
                 </body>
                 </html>
                 """)

    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title,
                               description = context.description,
                               body = context.body)
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')


def view_library(context, request):
    s = Template(u"""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Library $name</title>
                 </head>
                 <body>
                 <p>BC:</p>$breadcrumbs
                 <hr>
                 <h3>title: $title</h3>
                 <hr>
                 <p>Leaves:</p>$keys
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

def view_libcategory(context, request):
    s = Template(u"""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Категория $name</title>
                 </head>
                 <body>
                 <p>BC:</p>$breadcrumbs
                 <hr>
                 <h3>Категория: $title</h3>
                 <hr>
                 <h3>Книги</h3>
                 $books_data
                 </body>
                 </html>
                 """)

    data = []

    # select data from db
    dbname = context.__parent__.dbname
    with sqlite3.connect(dbname,
            detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""SELECT title, author, publisher,
                    year FROM books WHERE category LIKE ?""", (context.id,))
        rows = cur.fetchall()
        data = [{'title': i['title'],
                 'author': i['author'],
                 'publisher': i['publisher'],
                 'year': i['year']} for i in rows]
    if data:
        books_from_db = make_table_books(data)
    else:
        books_from_db = u'Нет книжек'

    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title,
                               books_data = books_from_db)

    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')

############################################################
# resources tree
#
RTREE = SiteFolder(title=u'Library 1')

folder1 = Folder(title=u'Folder one')
RTREE[u'f1'] = folder1

folder2 = RTREE[u'f2'] = Folder(title=u'Folder two')

d1 = Document(title=u'document 1',
              description=u'No description',
              body=u'<p>Body of testing document 1</p>')
folder1[u'd1'] = d1

d2 = Document(title=u'document 2',
              description=u'No description also',
              body=u'<p>Body of testing document 2</p>')
folder1[u'd2'] = d2

library = Library(title=u'Библиотека',
                 db=dbfilename)
RTREE[u'lib'] = library






if __name__ == '__main__':
    config = Configurator(root_factory=get_root)

    config.add_view(view=view_site,
                    context=SiteFolder)

    config.add_view(view=view_folder,
                    context=Folder)

    config.add_view(view=view_doc,
                    context=Document)

    config.add_view(view=view_library,
                    context=Library)
    config.add_view(view=view_libcategory,
                    context=LibCategory)



    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
