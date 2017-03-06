# -*- coding: utf-8 -*-
# see: http://docs.zope.org/zope.interface/
############################################################
from zope.interface import Interface
from zope.interface import implementer
from zope.component import getGlobalSiteManager
from zope.component import getUtility


class IGreeter(Interface):
    def greet(name):
        """Say hello to name"""
    def supergreet(name):
        """Say super hello to name"""

@implementer(IGreeter)
class Greeter:
    def greet(self, name):
        return "Hello %s" % name
    def supergreet(self, name):
        return "Super puper hello %s" % name.upper()

def main():
    lst = ('Andrey', 'Irina', 'Ivan', 'ебанько')

    greeter = getUtility(IGreeter, 'one')

    for name in lst:
        print(greeter.greet(name))

    for name in lst:
        print(greeter.supergreet(name))
    

gsm = getGlobalSiteManager()
gsm.registerUtility(Greeter(), IGreeter, 'one')

if __name__ == '__main__':
    main()
