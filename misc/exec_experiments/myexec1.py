# -*- coding: utf-8 -*-
############################################################
"""
Эксперименты с exec(object [,globals[, locals]])

"""
import io


g1 = {}
l1 = {'x': 10}
codestr1 = """print('value x={}'.format(x))"""


def df(ddict):
    out = io.StringIO()
    dkeys = sorted([i for i in ddict if not any((callable(ddict[i]),
                                             i.startswith('_')))])
    for k in dkeys:
        vv = repr(ddict.get(k))
        print('{key:<16} : {value:<30}'.format(key=k,
                                             value=vv),
              file=out)
    return out.getvalue()



def do_exec(code, g=None, l=None):
    cglobals = g if g else globals()
    clocals = l if l else locals()

    print('Before exec:')
    print(20 * '=')
    print('cglobals:\n\n{}\n'.format(df(cglobals)))
    print('clocals:\n\n{}\n'.format(df(clocals)))
    print('Executing...')
    print(80 * '-')

    exec(code, cglobals, clocals)

    print(80 * '-')
    print('After exec:')
    print(20 * '=')
    print('cglobals:\n\n{}\n'.format(df(cglobals)))
    print('clocals:\n\n{}\n'.format(df(clocals)))


def main():
    # do_exec(codestr1, g1, l1)
    # do_exec('y = 3.3', g1, l1)
    # do_exec('y = 3.3')
    do_exec('''y = 3.3
            print(y)
            print(y * 3)''')


if __name__ == '__main__':
    main()
