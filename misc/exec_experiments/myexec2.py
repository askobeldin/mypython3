# -*- coding: utf-8 -*-
############################################################
"""
Эксперименты с exec(object [,globals[, locals]])

"""
import io
import textwrap


# g1 = {}
# l1 = {'x': 10}
# codestr1 = """print('value x={}'.format(x))"""


prepare = lambda code: textwrap.dedent(code.expandtabs(4))

shorten = lambda text, nn: textwrap.shorten(text, nn, placeholder='...')



def prd(ddict):
    """Prints dict like object
    """
    ############################
    # pretty output
    #
    # column widths
    columns = (20, 40)

    header_line = '| '.join(['{:^%s}' % i for i in columns])
    data_line = '| '.join(['{:<%s}' % i for i in columns])
    header = header_line.format('Key', 'Value')
    out = io.StringIO()
    # dkeys = sorted([i for i in ddict if not any((callable(ddict[i]),
                                             # i.startswith('_')))])
    dkeys = sorted([i for i in ddict])
    print('-' * len(header), file=out)
    print(header, file=out)
    print('-' * len(header), file=out)
    for k in dkeys:
        vv = repr(ddict.get(k))
        print(data_line.format(k, shorten(vv, columns[1])), file=out)
    return out.getvalue()



def do_exec(code, g=None, l=None):
    cglobals = g if g else globals()
    clocals = l if l else locals()

    print('Before exec:')
    print('cglobals')
    print(prd(cglobals))
    print('clocals')
    print(prd(clocals))

    print('\n\nExecuting...')
    print(50 * '#')
    exec(code, cglobals, clocals)
    print(50 * '#')

    print('\nAfter exec:')
    print('cglobals')
    print(prd(cglobals))
    print('clocals')
    print(prd(clocals))


class Foo:
    def __init__(self):
        self.param = 'class Foo here'
        self.buf = []
    def add(self, item):
        self.buf.append(item)
    def addn(self, item, n):
        for _ in range(n):
            self.add(item)
    def astext(self):
        return self.param + ': ' + ', '.join([str(i) for i in self.buf])


def main():
    # do_exec(prepare("""
                    # print('test epta!')
                    # x = 'test '
                    # y = 4
                    # print(x * y)
                    # """), {}, {})

    a = Foo()
    print(locals())
    do_exec(prepare("""
                    add('a')
                    add('b')
                    addn('c', 4)
                    print(a.astext())
                    """),
            dict(vars(Foo)),
            )

if __name__ == '__main__':
    main()
