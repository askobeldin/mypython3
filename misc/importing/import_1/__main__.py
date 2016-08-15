# -*- coding: utf-8 -*-
#
################################################################################
import os
import sys


if __package__ == '':
    path = os.path.dirname(os.path.dirname(__file__))
    sys.path.insert(0, path)


import import_1


if __name__ == '__main__':
    sys.exit(import_1.main())
