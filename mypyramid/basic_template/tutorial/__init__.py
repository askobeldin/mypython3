# -*- coding: utf-8 -*-
############################################################
from pyramid.config import Configurator

from .resources import get_root, Resource
from .views import resource_view


def main(global_config, **settings):
    config = Configurator(settings=settings,
                          root_factory=get_root)
    config.add_view(resource_view, context=Resource)
    return config.make_wsgi_app()
