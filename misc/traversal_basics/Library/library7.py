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
from pyramid.httpexceptions import HTTPBadRequest
from pyramid.traversal import (resource_path,
                               traverse,
                               find_resource)
from pyramid.decorator import reify

#######################################
# configs
#
DEBUG = False

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

    def rename(self, title, href):
        self.title = title
        self.href = href
        # save data to DB
        dbname = self.__parent__.dbname
        with sqlite3.connect(dbname,
                detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("""UPDATE categories SET title = ?, href = ? WHERE id
                       LIKE ?""", (self.title, self.href, self.id))
            conn.commit()


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
        self.load_categories_from_db()

    def load_categories_from_db(self):
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
            data.sort(cmp=lambda x, y: cmp(x.lower(), y.lower()),
                      key=lambda x: x['title'])
            # make categories
            for item in data:
                self[item['href']] = LibCategory(item)

    def reload_categories_from_db(self):
        self.clear()
        self.load_categories_from_db()

    def add_category(self, title, href):
        # save data to DB
        with sqlite3.connect(self.dbname,
                detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("""INSERT INTO categories(title, href) VALUES(?,?)""",
                       (title, href))
            conn.commit()

    def addbook(self, title, author, publisher, year, category):
        # save book data to DB
        with sqlite3.connect(self.dbname,
                detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("""INSERT INTO books(title, author, publisher, year, category) VALUES(?,?,?,?,?)""",
                        (title,
                         author,
                         publisher,
                         year,
                         int(category)))
            conn.commit()



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


def makecategorieslist(request):
    catlst = [(v.id, v.title)
              for k, v in request.context.items()
              if isinstance(v, LibCategory)]
    options = [u'<option value="%s">%s</option>' % item
               for item in catlst]
    return u'<select name="category">' + u''.join(options) + u'</select>'


def isvalidcategory(request, category):
    catlst = [v.id for k, v in request.context.items()
              if isinstance(v, LibCategory)]
    # catlst = [2, 3, 4, 5]
    cat = int(category)
    return cat in catlst



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
                 <p>Категории:</p>$keys
                 <hr>
                 <h3>Actions:</h3>
                 <p>$addcategorylink</p>
                 <p>$addbooklink</p>
                 </body>
                 </html>
                 """)
    addcatlink = ''.join(['<a href=\"',
                          request.resource_url(context, '@@addcategory'),
                          '\">',
                          u'Add category',
                          '</a>'])
    addbooklink = ''.join(['<a href=\"',
                          request.resource_url(context, '@@addbook'),
                          '\">',
                          u'Add book',
                          '</a>'])
    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title,
                               keys = getFolderLeaves(request),
                               addcategorylink = addcatlink,
                               addbooklink = addbooklink)
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')


def library_add_cat_get(context, request):
    # method GET - return form
    s = Template(u"""
                     <!DOCTYPE html>
                     <html>
                     <head>
                     <title>Новая категория: $name</title>
                     </head>
                     <body>
                     <p>BC: $breadcrumbs</p>
                     <hr>
                     <h3>Создание новой категории</h3>
                     <hr>
                     <form action="" method="post">
                         <label><input type="text" maxlength="100" name="title"
                 id="cattitle">Наименование</label>
                         <label><input type="text" maxlength="100" name="href"
                 id="cathref">Имя</label>
                         <input type="submit" value="ADD">
                     </form>
                     </body>
                     </html>
                     """)
    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                                   name = context.__name__)
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')


def library_add_cat_post(context, request):
    # handle form`s data
    ptitle = request.POST.get('title', None)
    phref = request.POST.get('href', None)
    # XXX: validate

    if ptitle and phref:
        # add category to DB
        context.add_category(ptitle, phref)
        # reload categories from DB
        context.reload_categories_from_db()
        # goto to Library
        newurl = resource_path(context)
        return HTTPFound(newurl)
    else:
        # sent not filled form
        s = Template(u"""
                     <!DOCTYPE html>
                     <html>
                     <head>
                     <title>Error!</title>
                     </head>
                     <body>
                     <p>BC: $breadcrumbs</p>
                     <hr>
                     <h1>Необходимо заполнить форму</h1>
                     </body>
                     </html>
                     """)
        output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request))
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
                 <hr>
                 <h3>Actions:</h3>
                 <p>$renamelink</p>
                 </body>
                 </html>
                 """)
    renamelink = ''.join(['<a href=\"',
                          request.resource_url(context, '@@rename'),
                          '\">',
                          u'Rename category',
                          '</a>'])
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
                               books_data = books_from_db,
                               renamelink = renamelink)
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')


def library_add_book_get(context, request):
    # method GET - return form
    s = Template(u"""
                     <!DOCTYPE html>
                     <html>
                     <head>
                     <title>Add book: $name</title>
                     </head>
                     <body>
                     <p>BC: $breadcrumbs</p>
                     <hr>
                     <h3>Добавление книги</h3>
                     <hr>
                     <form action="" method="post">
                         <label><input type="text" maxlength="100" name="title"
                 id="booktitle">Наименование</label><br>
                         <label><input type="text" maxlength="100" name="author"
                 id="bookauthor">Автор</label><br>
                         <label><input type="text" maxlength="100" name="publisher"
                 id="bookpublisher">Издательство</label><br>
                         <label><input type="text" maxlength="100" name="year"
                 id="bookyear">Год издания</label><br>
                 $categories
                 <br>
                         <input type="submit" value="Add book">
                     </form>
                     </body>
                     </html>
                     """)
    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               categories = makecategorieslist(request))
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')


def library_add_book_post(context, request):
    # method POST - handle form
    ptitle = request.POST.get('title', None)
    pauthor = request.POST.get('author', None)
    ppublisher = request.POST.get('publisher', None)
    pyear = request.POST.get('year', None)
    pcategory = request.POST.get('category', None)
    # XXX: validate
    if ptitle and pcategory:
        # save record to db 
        print 20 * '='
        print 'save book: %s' % (ptitle,)
        print 'author: %s' % pauthor
        print 'publisher: %s' % ppublisher
        print 'year: %s' % pyear
        print 'category: %s' % pcategory, type(pcategory)
        print 20 * '='

        if isvalidcategory(request, pcategory):
            context.addbook(title=ptitle,
                            author=pauthor,
                            publisher=ppublisher,
                            year=pyear,
                            category=pcategory)
        else:
            # error - wrong category id
            raise HTTPBadRequest
        # goto to Library
        newurl = resource_path(context)
        return HTTPFound(newurl)
    else:
        s = Template(u"""
                     <!DOCTYPE html>
                     <html>
                     <head>
                     <title>Error!</title>
                     </head>
                     <body>
                     <p>BC: $breadcrumbs</p>
                     <hr>
                     <h1>Необходимо заполнить форму</h1>
                     </body>
                     </html>
                     """)
        output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request))
        return Response(body=output,
                       charset='utf-8',
                       content_type='text/html',
                       content_language='ru')






def category_rename_get(context, request):
    # method GET - return form
    s = Template(u"""
                     <!DOCTYPE html>
                     <html>
                     <head>
                     <title>Переименование категории: $name</title>
                     </head>
                     <body>
                     <p>BC: $breadcrumbs</p>
                     <hr>
                     <h3>Переименование категории</h3>
                     <hr>
                     <form action="" method="post">
                         <label><input type="text" maxlength="100" name="title"
                 id="cattitle" value="$title">Наименование</label>
                         <label><input type="text" maxlength="100" name="href"
                 id="cathref" value="$href">Имя</label>
                         <input type="submit" value="Rename">
                     </form>
                     </body>
                     </html>
                     """)
    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title,
                               href = context.href)
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')


def category_rename_post(context, request):
    # method POST - handle form
    ptitle = request.POST.get('title', None)
    phref = request.POST.get('href', None)
    # XXX: validate
    if ptitle and phref:
        library = context.__parent__
        # update record in db 
        # print 20 * '='
        # print 'update category to: %s' % (ptitle,)
        # print 20 * '='
        # save category to DB
        context.rename(ptitle, phref)
        # update categories
        library.reload_categories_from_db()

        # goto to Library
        # newurl = resource_path(library)

        # goto renamed category
        newurl = resource_path(find_resource(library, phref))
        return HTTPFound(newurl)
    else:
        s = Template(u"""
                     <!DOCTYPE html>
                     <html>
                     <head>
                     <title>Error!</title>
                     </head>
                     <body>
                     <p>BC: $breadcrumbs</p>
                     <hr>
                     <h1>Необходимо заполнить форму</h1>
                     </body>
                     </html>
                     """)
        output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request))
        return Response(body=output,
                       charset='utf-8',
                       content_type='text/html',
                       content_language='ru')





############################################################
# resources tree
#
RTREE = SiteFolder(title=u'Library 1')

folder1 = Folder(title=u'Folder one')
RTREE['f1'] = folder1

folder2 = RTREE['f2'] = Folder(title=u'Folder two')

d1 = Document(title=u'document 1',
              description=u'No description',
              body=u'<p>Body of testing document 1</p>')
folder1['d1'] = d1

d2 = Document(title=u'document 2',
              description=u'No description also',
              body=u'<p>Body of testing document 2</p>')
folder1['d2'] = d2

library = Library(title=u'Библиотека',
                 db=dbfilename)
RTREE['lib'] = library






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
    config.add_view(view=library_add_cat_get,
                    name='addcategory',
                    request_method='GET',
                    context=Library)
    config.add_view(view=library_add_cat_post,
                    name='addcategory',
                    request_method='POST',
                    context=Library)
    config.add_view(view=library_add_book_get,
                    name='addbook',
                    request_method='GET',
                    context=Library)
    config.add_view(view=library_add_book_post,
                    name='addbook',
                    request_method='POST',
                    context=Library)

    config.add_view(view=view_libcategory,
                    context=LibCategory)
    config.add_view(view=category_rename_get,
                    name='rename',
                    request_method='GET',
                    context=LibCategory)
    config.add_view(view=category_rename_post,
                    name='rename',
                    request_method='POST',
                    context=LibCategory)


    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
