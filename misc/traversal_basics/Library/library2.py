#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
################################################################################
from string import Template
import collections

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.location import lineage

from pyramid.httpexceptions import HTTPFound
from pyramid.traversal import (resource_path,
                               traverse,
                               find_resource)
from pyramid.decorator import reify


class MyContainer(collections.MutableMapping):
    __parent__ = __name__ = None

    def __init__(self):
        self.ckeys = collections.deque()
        self.container = {}

    def __getitem__(self, key):
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


class Library(MyContainer):
    def __init__(self, title, categories):
        super(Library, self).__init__()
        self.title = title
        # init categories containers
        for c in categories:
            self[c['href']] = Folder(title=c['title'])


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

############################################################
# views
#
def view_site(context, request):
    s = Template("""
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
    s = Template("""
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
    s = Template("""
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
    s = Template("""
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

############################################################
# library categories of books
CATEGORIES = [
    {'id': 1,
     'title': u'C++',
     'href': 'cpp'},
    {'id': 2,
     'title': u'python',
     'href': 'python'},
    {'id': 3,
     'title': u'васик',
     'href': 'vasik'},
]


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
                 categories=CATEGORIES)
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



    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
