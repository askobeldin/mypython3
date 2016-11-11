#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
################################################################################
"""

"""
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response


class Resource(dict):
    pass


def get_root(request):
    # return Resource({'a': Resource({'b': Resource({'c': Resource()})})})
    return GD


def hello_world_of_resources(context, request):
    output = "Here's a resource and its children: %s" % context
    # ----------
    # print '### request:', request

    print 60 * '='
    print 'context info'
    print
    for i in context:
        print i, context[i]

    print 60 * '='
    print 'URL parameters'
    print

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


    return Response(output)


# ------------------------------
# tree
GD = Resource(
    {'a': Resource({'b': Resource({'c': Resource()})}),
     'd': Resource(),
     'e': Resource()
    }
)




if __name__ == '__main__':
    config = Configurator(root_factory=get_root)

    config.add_view(hello_world_of_resources, context=Resource)

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
