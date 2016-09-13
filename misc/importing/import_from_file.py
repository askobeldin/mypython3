# -*- coding: utf-8 -*-
#
################################################################################
"""
How can I load a Python module given its full path?
Note that the file can be anywhere in the filesystem,
as it is a configuration option.
-----------------------------------------------------------

For Python 3.5+ use:
-------------------
import importlib.util
spec = importlib.util.spec_from_file_location("module.name", "/path/to/file.py")
foo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(foo)
foo.MyClass()



For Python 3.3 and 3.4 use:
--------------------------
from importlib.machinery import SourceFileLoader

foo = SourceFileLoader("module.name", "/path/to/file.py").load_module()
foo.MyClass()
"""
