# -*- coding: utf-8 -*-
############################################################
import collections


class MyContainer(collections.MutableMapping):
    __parent__ = __name__ = None
    def __init__(self):
        self.ckeys = collections.deque()
        self.container = {}
    def __getitem__(self, key):
        try:
            item = self.container[key]
            return item
        except KeyError as e:
            raise
    def __setitem__(self, key, value):
        if key in self.ckeys:
            self.container[key] = value
        else:
            self.ckeys.append(key)
            self.container[key] = value
        value.__name__ = key
        value.__parent__ = self
    def __delitem__(self, key):
        if key in self.ckeys:
            self.ckeys.remove(key)
            del self.container[key]
        else:
            raise KeyError
    def __len__(self):
        return len(self.ckeys)
    def __iter__(self):
        return iter(self.ckeys)


class Resource(MyContainer):
    def __init__(self, title):
        super(Resource, self).__init__()
        self.title = title


########################################
# Resources tree
#
TREE = Resource('root')

TREE['a'] = Resource('this is A resource')
TREE['a']['e'] = Resource('ресурс E')
TREE['a']['g'] = Resource('ресурс G')
TREE['a']['f'] = Resource('а это ресурс F')
TREE['b'] = Resource('This is B')
TREE['b']['e'] = Resource('This is BE epta!')
TREE['c'] = Resource('Охуенно, а это ресурс C')
TREE['c']['h'] = Resource('h')
########################################

def get_root(request):
    return TREE
