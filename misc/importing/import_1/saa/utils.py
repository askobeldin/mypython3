# -*- coding: utf-8 -*-
#
################################################################################
"""
import inspect
def f1(): f2()

def f2():
    curframe = inspect.currentframe()
    calframe = inspect.getouterframes(curframe, 2)
    print 'caller name:', calframe[1][3]

f1()
caller name: f1

####################################################
import inspect
# functions
def whoami():
    return inspect.stack()[1][3]
def whosdaddy():
    return inspect.stack()[2][3]
def foo():
    print "hello, I'm %s, daddy is %s" % (whoami(), whosdaddy())
    bar()
def bar():
    print "hello, I'm %s, daddy is %s" % (whoami(), whosdaddy())

johny = bar
# call them!
foo()
bar()
johny()

output:
hello, I'm foo, daddy is ?
hello, I'm bar, daddy is foo
hello, I'm bar, daddy is ?
hello, I'm bar, daddy is ?

"""

def util1(msg):
    data = 'Call {modulename}.util1 with {msg}'
    print(data.format(modulename=__name__,
                      msg=msg))
