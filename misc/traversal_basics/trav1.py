#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
################################################################################
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
    # print 'request:', request
    print 'request PATH_INFO:', request['PATH_INFO']
    for i in context:
        print i, context[i]

    return Response(output)


# ------------------------------
# tree
GD = Resource(
    {'a': Resource({'b': Resource({'c': Resource()})}),
     'd': Resource(),
     'e': Resource()}
)


if __name__ == '__main__':
    config = Configurator(root_factory=get_root)

    config.add_view(hello_world_of_resources, context=Resource)

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
