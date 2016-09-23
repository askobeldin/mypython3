# -*- coding: utf-8 -*-
############################################################
import sys


from pyramid.config import Configurator

from .resources import get_root, Resource
from .views import resource_view


from foo.data import Foo


def main(global_config, **settings):
    config = Configurator(settings=settings,
                          root_factory=get_root)
    config.add_view(resource_view, context=Resource)
    ###########
    print('sys.path:')
    for e in sys.path: print(e)
    a = Foo()
    print('\nmy data from Foo')
    print(a.a)
    print(type(a))
    ###########
    return config.make_wsgi_app()
