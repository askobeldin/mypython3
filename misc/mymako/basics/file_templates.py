# -*- coding: utf-8 -*-
#
###############################################################################
"""Try to use file based templates
"""
import os.path
import types
import io

from mako.template import Template
from mako.lookup import TemplateLookup


mkabspath = lambda *chunks: os.path.abspath(os.path.join(*list(chunks)))

try:
    CURDIR = os.path.dirname(__file__)
except NameError:
    import os
    CURDIR = os.getcwd()

pathways = types.SimpleNamespace()

def serve_template(templatename, lookup, **kwargs):
    mytemplate = lookup.get_template(templatename)
    print(mytemplate.render(**kwargs), end='')

def render_template(templatename, lookup, **kwargs):
    mytemplate = lookup.get_template(templatename)
    return mytemplate.render(**kwargs)

# templates subfolder
pathways.templates = mkabspath(CURDIR, 'templates')
# cache for templates
pathways.cache = mkabspath(CURDIR, '.cache')

mylookup = TemplateLookup(directories=[pathways.templates],
                          input_encoding='utf-8',
                          module_directory=pathways.cache)

print('templates: {}'.format(pathways.templates))
print('cache: {}'.format(pathways.cache))

output = io.StringIO()

print('rendering template1.mktxt\n================================')

print(render_template('mytemplate1.mktxt', lookup=mylookup), end='',
      file=output)
print(output.getvalue(), end='')
