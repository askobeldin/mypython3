# -*- coding: utf-8 -*-
#
################################################################################
# http://eli.thegreenplace.net/2015/redirecting-all-kinds-of-stdout-in-python
#
from contextlib import redirect_stdout
import ctypes
import io
import os




f = io.StringIO()
with redirect_stdout(f):
    print('foobar')
    print(12)
    # libc.puts(b'this comes from C')
    # os.system('echo and this is from echo')
print('got stdout: "{0}"'.format(f.getvalue()))

