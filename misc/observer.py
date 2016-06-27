# -*- coding: utf-8 -*-
############################################################
"""
Observer pattern
Key 1: Spreading information to all listeners.

This is the basic pattern in which an object tells other objects about
something interesting. It is very useful in GUI applications, pub/sub
applications, and those applications where we need to notify a lot of
loosely-coupled application components about a change occurring at one source
node. In the following code, Subject is the object to which other objects
register themselves for events via register_observer . The observer objects
are the listening objects. The observers start observing the function that
registers the observers object to Subject object.  Whenever there is an event
to Subject it cascades the event to all observers :
"""
import weakref


class Subject(object):
    """Provider of notifications to other objects
    """
    def __init__(self, name):
        self.name = name
        self._observers = weakref.WeakSet()

    def register_observer(self, observer):
        """attach the observing object for this subject
        """
        self._observers.add(observer)
        print("observer {0} now listening on {1}".format(
        observer.name, self.name))

    def notify_observers(self, msg):
        """transmit event to all interested observers
        """
        print("subject notifying observers about {}".format(msg,))
        for observer in self._observers:
            observer.notify(self, msg)


class Observer(object):
    def __init__(self, name):
        self.name = name

    def start_observing(self, subject):
        """register for getting event for a subject
        """
        subject.register_observer(self)

    def notify(self, subject, msg):
        """notify all observers
        """
        print("{0} got msg from {1} that {2}".format(self.name,
                                                     subject.name,
                                                     msg))


class_homework = Subject("class homework")
student1 = Observer("student 1")
student2 = Observer("student 2")

student1.start_observing(class_homework)
student2.start_observing(class_homework)

class_homework.notify_observers("result is out")

del student2

class_homework.notify_observers("20/20 passed this sem")
