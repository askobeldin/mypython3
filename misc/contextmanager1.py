# -*- coding: utf-8 -*-
#
################################################################################
import contextlib


@contextlib.contextmanager
def looking_glass():
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    msg = ''  # <1>
    try:
        yield 'JABBERWOCKY'
    except ZeroDivisionError:  # <2>
        msg = 'Please DO NOT divide by zero!'
    finally:
        sys.stdout.write = original_write  # <3>
        if msg:
            print(msg)  # <4>


print('Alice, Kitty and Snowdrop')

with looking_glass() as what:
    print('Alice, Kitty and Snowdrop')
    print(what)
