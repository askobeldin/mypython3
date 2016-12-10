# -*- coding: utf-8 -*-
#
###############################################################################
from .reader import *

#  __all__ = (reader.__all__,)
__all__ = ('Convertor', )


class Convertor:
    def __init__(self):
        pass
    def convertfile(self, filename, encoding='utf-8'):
        return tuple(items(filename, encoding))
