# -*- coding: utf-8 -*-
#
################################################################################

class foo:
    def __init__(self):
        self.x = 'this is X'
    def getinfo(self):
        print('globals() in class foo:\n{}'.format(globals()))
        print('locals() in class foo:\n{}'.format(locals()))



def main():

    x = foo()
    x.getinfo()

    print('globals():\n{}'.format(globals()))
    print('locals():\n{}'.format(locals()))

if __name__ == '__main__':
    main()
