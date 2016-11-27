# -*- coding: utf-8 -*-
###############################################################################
from os.path import isdir, exists
from os.path import (abspath,
                     join,
                     basename,
                     splitext,
                     dirname,
                     expanduser)
from glob import glob



############################
def getfiles(folder, extension):
    names = [path for path in glob(abspath(join(folder, extension)))]
    return [path for path in names if all((exists(path),))]

