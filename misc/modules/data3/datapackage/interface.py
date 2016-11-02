# This module implements the public interface for the "datapackage" directory.
#
# This demonstrates how a Python package can contain data files, which can then
# be accessed as desired.

import os.path

from .globals import _phone_numbers

def get_phone_numbers():
    print('calling get_phone_numbers')
    global _phone_numbers
    return _phone_numbers

