#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
################################################################################
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from string import Template

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.location import lineage

"""
from pyramid.httpexceptions import HTTPFound

#################################
            # form is valid
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



class Folder(dict):
    def __init__(self, name, parent, title):
        self.__name__ = name
        self.__parent__ = parent
        self.title = title
    ##################################################
    # testing of __getitem__
    #
    def __getitem__(self, key):
        print '*** calling Folder.__getitem__(%s)' % key
        # в случае отсутствия ключа будет сгенерирован новый документ
        try:
            item = super(Folder, self).__getitem__(key)
        except KeyError:
            gtitle = u'Generated document %s' % key
            gbody = u'Generated body for document %s' % key
            item = Document(str(key), self, gtitle, gbody)
            print '=== Generating new document %s ===' % key
            ##############################################
            # сохранение сгенерированного документа в БД
            self[key] = item

        return item

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


class Collector(Folder):
    def __init__(self, *args, **kwds):
        super(Collector, self).__init__(*args, **kwds)
        self.toysList = []


class Toy(object):
    __slots__ = ('__name__', '__parent__',
                 'title', 'description', 'tag')
    def __init__(self, data, parent):
        self.__name__ = data['title']
        self.__parent__ = parent
        self.title = data['title']
        self.description = data['description']
        self.tag = data['tag']


class SimpleDB(OrderedDict):
    def __init__(self, name, parent, title):
        super(SimpleDB, self).__init__()
        self.__name__ = name
        self.__parent__ = parent
        self.title = title



def get_root(request):
    return RTREE


def view_site(context, request):
    s = Template("""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Site folder</title>
                 </head>
                 <body>
                 <h3>title: $title</h3>
                 <p>Leaves: $keys</p>
                 </body>
                 </html>
                 """)
    # output = s.safe_substitute(title = context.title,
                               # keys = context.keys())
    output = s.safe_substitute(title = context.title,
                               keys = getFolderLeaves(request))

    # for i in context.items():
        # print i
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


# def view_folder2(context, request):
    # output2 = u"Folder -> %s\nKeys: %s" % (context.title, context.keys())
    # output = getBreadCrumbs(request) + output2
    # return Response(body=output,
                   # charset='utf-8',
                   # content_type='text/html',
                   # content_language='ru')


def view_collector(context, request):
    s = Template("""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Collector $name</title>
                 </head>
                 <body>
                 <p>BC: $breadcrumbs</p>
                 <hr>
                 <h3>title: $title</h3>
                 <hr>
                 <h3>Toys:</h3>
                 $toys
                 </body>
                 </html>
                 """)

    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title,
                               toys = getToysTableLinks(context, request))

    # -----
    # print request.resource_url(simpledb['3'])
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
                 <h3>title: $title</h3>
                 <p>body: $body</p>
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


def view_db(context, request):
    s = Template("""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Database $name</title>
                 </head>
                 <body>
                 <p>BC: $breadcrumbs</p>
                 <hr>
                 <h3>title: $title</h3>
                 <hr>
                 </body>
                 </html>
                 """)

    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title)

    # OK
    #
    # print 'context: ', context
    # print 'context[\'3\']=', context['3']
    return Response(body=output,
                   charset='utf-8',
                   content_type='text/html',
                   content_language='ru')


def view_toy(context, request):
    s = Template("""
                 <!DOCTYPE html>
                 <html>
                 <head>
                 <title>Toy $name</title>
                 </head>
                 <body>
                 <p>BC: $breadcrumbs</p>
                 <hr>
                 <h3>Title: $title</h3>
                 <h3>Tag: $tag</h3>
                 <h3>Description:</h3>
                 <p>$descr</p>
                 <hr>
                 </body>
                 </html>
                 """)

    output = s.safe_substitute(breadcrumbs = getBreadCrumbs(request),
                               name = context.__name__,
                               title = context.title,
                               descr = context.description,
                               tag = context.tag)
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
    li = ['<li>'  + '<a href="' + request.resource_url(i[1]) + '">' + i[0] + '</a></li>'
          for i in leaves]
    return "<ul>" + "\n".join(li) + "</ul>"


def getToysList(collector):
    if collector.toysList:
        return collector.toysList
    else:
        return []


def getToysTable(collector):
    table = u"""
    <table>
    <tbody>
    <tr>
    """
    lst = [table]

    if collector.toysList:
        # return collector.toysList
        for i in collector.toysList:
            lst.append(u"<td>%s</td>" % i)

        lst.append(u"</tr></tbody></table>")
        return "".join(lst)
    else:
        return ""


def getToysTableLinks(collector, request):
    table = u"""
    <table>
    <tbody>
    <tr>
    """
    lst = [table]

    if collector.toysList:
        # return collector.toysList
        for i in collector.toysList:
            lst.append(u"<td><a href=\"/db/%s\">%s</a></td>" % (i, i))

        lst.append(u"</tr></tbody></table>")
        return "".join(lst)
    else:
        return ""



def fillCollector(collector, tag, db):
    lst = []
    data = db.items()
    for (k, v) in data:
        if v['tag'] == tag:
            lst.append(k)
    collector.toysList.extend(lst)



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
    print 60 * '='
    print 'context info'
    print
    for i in context:
        print i, context[i]

    print 60 * '='
    print 'URL parameters'








################
# resources tree
#
RTREE = SiteFolder('', None, u'Site folder')

folder1 = Folder(u'f1', RTREE, u'Folder one')
# RTREE[u'f1'] = folder1
RTREE[u'f1'] = folder1

folder2 = RTREE[u'f2'] = Folder(u'f2', RTREE, u'Folder two')
folder3 = RTREE[u'f3'] = Folder(u'f3', RTREE, u'Folder три')

folder4 = folder3[u'f4'] = Folder(u'f4', folder3, u'Folder #4')

d1 = Document(name=u'd1',
              parent=folder1,
              title=u'Testing document 1',
              body=u'Body of testing document 1')
folder1[u'd1'] = d1

# main toys collector
collector = RTREE[u'toys'] = Folder(u'toys', RTREE, u'Toys')

collector1 = collector[u'bears'] = Collector(u'bears', collector, u'Bears')
# fill in toys list
# collector1.toysList.extend(range(1, 10))

collector2 = collector[u'dolls'] = Collector(u'dolls', collector, u'Dolls')
# fill in toys list
# collector2.toysList.extend(range(10, 20))

collector3 = collector[u'angels'] = Collector(u'angels', collector, u'Angels')
# fill in toys list
# collector3.toysList.extend(range(20, 30))

collector4 = collector[u'test'] = Collector(u'test', collector, u'Testing')

simpledb = RTREE[u'db'] = SimpleDB(u'db', RTREE, u'SimpleDB')



PSEUDO_DB = {
    1: {'title': u'Bear 1', 'description': u'Description of Bear 1', 'tag': u'bears'},
    2: {'title': u'Doll 2', 'description': u'Description of Doll 2', 'tag': u'dolls'},
    3: {'title': u'Doll 3', 'description': u'Description of Doll 3', 'tag': u'dolls'},
    4: {'title': u'Bear 4', 'description': u'Description of Bear 4', 'tag': u'bears'},
    5: {'title': u'Doll 5', 'description': u'Description of Doll 5', 'tag': u'dolls'},
    6: {'title': u'Angel 6', 'description': u'Description of Angel 6', 'tag': u'angels'},
    7: {'title': u'Doll 7', 'description': u'Description of Doll 7', 'tag': u'dolls'},
    8: {'title': u'Doll 8', 'description': u'Description of Doll 8', 'tag': u'dolls'},
    9: {'title': u'Bear 9', 'description': u'Description of Bear 9', 'tag': u'bears'},
    10: {'title': u'Angel 10', 'description': u'Description of Angel 10', 'tag': u'angels'},
    11: {'title': u'Angel 11', 'description': u'Description of Angel 11', 'tag': u'angels'},
    12: {'title': u'Angel 12', 'description': u'Description of Angel 12', 'tag': u'angels'},
    13: {'title': u'Angel 13', 'description': u'Description of Angel 13', 'tag': u'angels'},
    14: {'title': u'Bear 14', 'description': u'Description of Bear 14', 'tag': u'bears'},
    15: {'title': u'Bear 15', 'description': u'Description of Bear 15', 'tag': u'bears'},
    16: {'title': u'Angel 16', 'description': u'Description of Angel 16', 'tag': u'angels'},
    17: {'title': u'Test 17', 'description': u'Description of Test 17', 'tag': u'test'},
    18: {'title': u'Test 18', 'description': u'Description of Test 18', 'tag': u'test'},
    19: {'title': u'Doll 19', 'description': u'Description of Doll 19', 'tag': u'dolls'},
    20: {'title': u'Test 20', 'description': u'Description of Test 20', 'tag': u'test'},
    21: {'title': u'Angel 21', 'description': u'Description of Angel 21', 'tag': u'angels'},
    22: {'title': u'Bear 22', 'description': u'Description of Bear 22', 'tag': u'bears'},
    23: {'title': u'Test 23', 'description': u'Description of Test 23', 'tag': u'test'},
    24: {'title': u'Doll 24', 'description': u'Description of Doll 24', 'tag': u'dolls'},
    25: {'title': u'Doll 25', 'description': u'Description of Doll 25', 'tag': u'dolls'},
    26: {'title': u'Test 26', 'description': u'Description of Test 26', 'tag': u'test'},
    27: {'title': u'Bear 27', 'description': u'Description of Bear 27', 'tag': u'bears'},
    28: {'title': u'Test 28', 'description': u'Description of Test 28', 'tag': u'test'},
    29: {'title': u'Angel 29', 'description': u'Description of Angel 29', 'tag': u'angels'},
    30: {'title': u'Test 30', 'description': u'Description of Test 30', 'tag': u'test'},
    31: {'title': u'Doll 31', 'description': u'Description of Doll 31', 'tag': u'dolls'},
}


###########################################################################
if __name__ == '__main__':

    config = Configurator(root_factory=get_root)

    config.add_view(view=view_site,
                    context=SiteFolder)

    config.add_view(view=view_folder,
                    context=Folder)

    config.add_view(view=view_collector,
                    context=Collector)

    # config.add_view(view=view_folder2,
                    # name='two',
                    # context=Folder)

    config.add_view(view=view_doc,
                    context=Document)

    config.add_view(view=view_db,
                    context=SimpleDB)

    config.add_view(view=view_toy,
                    context=Toy)

    # filling collectors of toys
    fillCollector(collector1, u'bears', PSEUDO_DB)
    fillCollector(collector2, u'dolls', PSEUDO_DB)
    fillCollector(collector3, u'angels', PSEUDO_DB)
    fillCollector(collector4, u'test', PSEUDO_DB)

    ########################################
    # initialize database
    switchcollector = {u'bears': collector1,
                       u'dolls': collector2,
                       u'angels': collector3,
                       u'test': collector4}

    for (k, v) in PSEUDO_DB.items():
        simpledb[str(k)] = Toy(data = v, parent = switchcollector[v['tag']])



    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
