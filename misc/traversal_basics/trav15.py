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
    pass


class MyObject1(object):
    def __init__(self, treenode, key, title):
        self.__name__ = key
        self.__parent__ = treenode
        self.title = title
        self.ListItems = [x for x in xrange(1, 11)]

        # make node in tree
        treenode[key] = self

    def shuffle(self):
        shuffle(self.ListItems)

    def append(self, item):
        self.ListItems.append(item)


class MyDBObject1(object):
    def __init__(self, items):
        self.DBList = []
        for i in items:
            self.DBList.append(i)

    def add(self, item):
        self.DBList.append(item)








###############################################################################
# views
#
#
def view_site(context, request):
    s = Template("""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Site</title>
                 </head>
                 <body>
                 <h3>title: $title</h3>
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


def view_myobject1(context, request):
    s = Template("""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>MyObject1: $name</title>
                 </head>
                 <body>
                 <p>BC: $breadcrumbs</p>
                 <hr>
                 <h3>Title: $title</h3>
                 <p>ListItems: $listitems</p>
                 <hr>
                 <a href= "$cmd">shuffle</a>
                 <hr>
                 <form action="">
                 <input type="text" maxlength="100" name="item">
                 <input type="hidden" name="cmd" value="append">
                 <input type="submit" value="ADD">
                 </form>
                 </body>
                 </html>
                 """)
    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title,
                               listitems = ','.join([unicode(x) for x in context.ListItems]),
                               cmd = request.resource_url(context) + '?cmd=shuffle')

    # handle simple command `shuffle` and `append` to this object
    if request.params:
        c = request.params.get('cmd', None)
        if c:
            print 'cmd is %s' % c
            if c == 'shuffle':
                print 'shuffle!'
                context.shuffle()
                url = request.resource_url(context)
                return HTTPFound(location=url)
            if c == 'append':
                item = request.params.get('item', 0)
                print 'append'
                context.append(item)
                url = request.resource_url(context)
                return HTTPFound(location=url)

    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')



def view_add_to_mydbobject1(context, request):
    s = Template("""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Add form to $name</title>
                 </head>
                 <body>
                 <hr>
                 <h3>title: $title</h3>
                 <hr>
                 <p>sdlfjsldf wofjwo</p>
                 </body>
                 </html>
                 """)
    output = s.safe_substitute(name = 'AAAADDD',
                               title = 'title here epta')
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')








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





def printinfo(context, request):
    # print request.__dict__

    formatstring ='%-36s%s'

    print formatstring % ('request.url', request.url)
    print formatstring % ('request.host', request.host)
    print formatstring % ('request.host_url', request.host_url)
    print formatstring % ('request.application_url', request.application_url)
    print formatstring % ('request.path_url', request.path_url)
    print formatstring % ('request.path', request.path)
    print formatstring % ('request.path_qs', request.path_qs)
    print formatstring % ('request.query_string', request.query_string)
    print 10 * '-'
    # print formatstring % ('request.matchdict', request.matchdict)
    ### need a name attribute
    # print formatstring % ('request.resource_url(context)', request.resource_url(context))
    print formatstring % ('request.cookies', request.cookies)
    print formatstring % ('request.headers', request.headers)
    # print formatstring % ('request.json', request.json)
    print formatstring % ('request.method', request.method)
    print formatstring % ('request.charset', request.charset)

    if request.params:
        print formatstring % ('request.params', request.params)
        print formatstring % ('request.params.keys()', request.params.keys())
        print formatstring % ('request.params.items()', request.params.items())
        # ошибка если передано несколько параметров age
        # print formatstring % ('request.params.getone(\'age\')', request.params.getone('age'))
        print formatstring % ('request.params.getall(\'age\')', request.params.getall('age'))
    # print 60 * '='
    # print 'context info'
    # print
    # for i in context:
        # print i, context[i]

    # print 60 * '='
    # print 'URL parameters'



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
RTREE = SiteFolder('', None, u'Site folder')


###############################################################################
# My application registry
#
APPREGISTRY = {}



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

    config.add_view(view=view_myobject1,
                    context=MyObject1)

    # config.add_view(view=view_myobject1_shuffle,
                    # context=MyObject1,
                    # name='shuffle')

    # config.add_view(view=view_add_to_mydbobject1,
                    # name='add',
                    # context=MyDBObject1)



    # make resources tree
    makeResourcesTree()

    # create and insert to resources tree my object
    #
    MyObject1(RTREE, 'o1', 'my object 1')
    MyObject1(RTREE, 'o2', 'my object 2')


    APPREGISTRY['dblist'] = MyDBObject1(('one',
                                         'two',
                                         'three',
                                         u'четыре',
                                         u'пять ептыть!'))

    # this document will contain data from MyDBObject1
    dlst = APPREGISTRY.get('dblist', None)
    if dlst:
        RTREE['ddb'] = Document(name='ddb',
                                parent=RTREE,
                                title=u'MyDBObject1 document',
                                body=mkHTMLfromList(dlst.DBList))




    # ----------------------------------------------------
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
