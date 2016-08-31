# -*- coding: utf-8 -*-
############################################################
from setuptools import setup

requires = [
    'pyramid',
    'pyramid_mako',
    'pyramid_debugtoolbar'
]

setup(name='project',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = project:main
      """,
)
