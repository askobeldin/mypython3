# -*- coding: utf-8 -*-
#
################################################################################
import inspect


def foo(arg):
    print('foo\'s arg is {!r}'.format(arg))



def main():
    # foo('test')
    print('-' * 80)
    print('Using inspect module:\n')
    print('inspect.isfunction(foo) is {!r}'.format(inspect.isfunction(foo)))
    print('signature is')
    sig = inspect.signature(foo)
    print(str(sig))
    print('signature.parameters is')
    print(sig.parameters)

    print('getsource is')
    print(inspect.getsource(foo))
    print('getsourcelines is')
    print(inspect.getsourcelines(foo))

    print('-' * 80)
    print('Using special methods:\n')
    print('foo.__name__ is {}'.format(foo.__name__))
    print('foo.__code__ is {}'.format(foo.__code__))
    print('foo.__code__.co_varnames is {}'.format(foo.__code__.co_varnames))
    print('foo.__code__.co_argcount is {}'.format(foo.__code__.co_argcount))

if __name__ == '__main__':
    main()
