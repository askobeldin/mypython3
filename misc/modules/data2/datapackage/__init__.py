# Package initialization file.
import os.path

from .interface import *

# global list of numbers
_phone_numbers = []


def _init():
    print('calling _init')
    global _phone_numbers
    # _phone_numbers = []
    cur_dir = os.path.abspath(os.path.dirname(__file__))
    file = open(os.path.join(cur_dir, "data", "phone_numbers.txt"))
    for line in file:
        _phone_numbers.append(line.strip())
    file.close()

# init global list
_init()
