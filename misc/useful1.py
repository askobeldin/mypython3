# -*- coding: utf-8 -*-
#
################################################################################
from .encoding import DEFAULT_ENCODING


def no_code(x, encoding=None):
    return x

def decode(s, encoding=None):
    encoding = encoding or DEFAULT_ENCODING
    return s.decode(encoding, "replace")

def encode(u, encoding=None):
    encoding = encoding or DEFAULT_ENCODING
    return u.encode(encoding, "replace")

def cast_unicode(s, encoding=None):
    if isinstance(s, bytes):
        return decode(s, encoding)
    return s

def cast_bytes(s, encoding=None):
    if not isinstance(s, bytes):
        return encode(s, encoding)
    return s

def buffer_to_bytes(buf):
    """Cast a buffer or memoryview object to bytes"""
    if isinstance(buf, memoryview):
        return buf.tobytes()
    if not isinstance(buf, bytes):
        return bytes(buf)
    return buf

if sys.version_info[0] >= 3:
    PY3 = True

    str_to_unicode = no_code
    unicode_to_str = no_code
    str_to_bytes = encode
    bytes_to_str = decode
    cast_bytes_py2 = no_code
    cast_unicode_py2 = no_code
    buffer_to_bytes_py2 = no_code

    string_types = (str,)
    unicode_type = str

    xrange = range
    def iteritems(d): return iter(d.items())
    def itervalues(d): return iter(d.values())
    getcwd = os.getcwd

    MethodType = types.MethodType

    def execfile(fname, glob, loc=None, compiler=None):
        loc = loc if (loc is not None) else glob
        with open(fname, 'rb') as f:
            compiler = compiler or compile
            exec(compiler(f.read(), fname, 'exec'), glob, loc)

else:
    PY3 = False

    str_to_unicode = decode
    unicode_to_str = encode
    str_to_bytes = no_code
    bytes_to_str = no_code
    cast_bytes_py2 = cast_bytes
    cast_unicode_py2 = cast_unicode
    buffer_to_bytes_py2 = buffer_to_bytes

    string_types = (str, unicode)
    unicode_type = unicode

    xrange = xrange
    def iteritems(d): return d.iteritems()
    def itervalues(d): return d.itervalues()
    getcwd = os.getcwdu

    def MethodType(func, instance):
        return types.MethodType(func, instance, type(instance))
################################################################################
"""
A simple utility to import something by its string name.
"""
# Copyright (c) IPython Development Team.
# Distributed under the terms of the Modified BSD License.

def import_item(name):
    """Import and return ``bar`` given the string ``foo.bar``.

    Calling ``bar = import_item("foo.bar")`` is the functional equivalent of
    executing the code ``from foo import bar``.

    Parameters
    ----------
    name : string
      The fully qualified name of the module/package being imported.

    Returns
    -------
    mod : module object
       The module that was imported.
    """
    if not isinstance(name, string_types):
        raise TypeError("import_item accepts strings, not '%s'." % type(name))
    name = cast_bytes_py2(name)
    parts = name.rsplit('.', 1)
    if len(parts) == 2:
        # called with 'foo.bar....'
        package, obj = parts
        module = __import__(package, fromlist=[obj])
        try:
            pak = getattr(module, obj)
        except AttributeError:
            raise ImportError('No module named %s' % obj)
        return pak
    else:
        # called with un-dotted string
        return __import__(parts[0])
