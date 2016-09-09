# -*- coding: utf-8 -*-
#
################################################################################
"""Try to use defs in templates
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

def render_template(templatename, lookup, **kwargs):
    mytemplate = lookup.get_template(templatename)
    return mytemplate.render(**kwargs)

# templates subfolder
pathways.templates = mkabspath(CURDIR, 'templates')
# cache for templates
pathways.cache = mkabspath(CURDIR, '.cache')

###################################
# main code
#
TEMPLATE = 'defs1.mktxt'

mylookup = TemplateLookup(directories=[pathways.templates],
                          input_encoding='utf-8',
                          module_directory=pathways.cache)

# print('templates: {}'.format(pathways.templates))
# print('cache: {}'.format(pathways.cache))

output = io.StringIO()

print(render_template(TEMPLATE, lookup=mylookup, x=30), file=output)

# prints if text line is not empty
# for line in output.getvalue().split('\n'):
    # line = line.strip()
    # if line:
        # print(line)

print(output.getvalue())
