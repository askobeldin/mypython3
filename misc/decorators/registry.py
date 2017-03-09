# -*- coding: utf-8 -*-
#
################################################################################
"""
Registry pattern
Key 9: Adding functionality from anywhere in code to class.

This is one of my favorite patterns and comes to help a lot. In this pattern,
we register classes to a registry, which tracks the naming to functionality.
Hence, we can add functionality to the main class from anywhere in the code. In
the following code, Convertor tracks all convertors from dictionary to Python
objects. We can easily add further functionalities to the system using the
convertor.register decorator from anywhere in the code, as follows:
"""

class ConvertError(Exception):
    """Error raised on errors on conversion"""
    pass


class Convertor(object):
    def __init__(self):
        """create registry for storing method mapping """
        self.__registry = {}

    def to_object(self, data_dict):
        """convert to python object based on type of dictionary"""
        dtype = data_dict.get('type', None)
        if not dtype:
            raise ConvertError("cannot create object, type not defined")
        elif dtype not in self.__registry:
            raise ConvertError("cannot convert type not registered")
        else:
            convertor = self.__registry[dtype]
            return convertor.to_python(data_dict['data'])

    def register(self, convertor):
        iconvertor = convertor()
        self.__registry[iconvertor.dtype] = iconvertor

convertor = Convertor()

class Person():
    """ a class in application """
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self,):
        return "<Person (%s, %s)>" % (self.name, self.age)


@convertor.register
class PersonConvertor(object):
    def __init__(self):
        self.dtype = 'person'

    def to_python(self, data):
        # not checking for errors in dictionary to instance creation
        p = Person(data['name'], data['age'])
        return p


print(convertor.to_object(
    {'type': 'person', 'data': {'name': 'arun', 'age': 12}}))

print(convertor.to_object(
    {'type': 'person', 'data': {'name': 'Ralf', 'age': 32}}))
