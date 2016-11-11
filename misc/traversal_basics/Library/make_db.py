#! /usr/bin/env python
# -*- coding: utf-8 -*-
############################################################
import os
import sqlite3
from sys import exit
# from datetime import datetime, timedelta
# from random import choice, randint, random


db_filename = 'library.db'
schema_filename = 'library.sql'


categories = (
    (u'C++', u'cpp'),
    (u'python', u'python'),
    (u'Жава', u'java'),
    (u'васик', u'basic'),
)

#    title, author, publisher, year, category
books = (
    (u'c++ in 21 days', u'Pupkin', u'Apress', u'1992', 1),
    (u'python in 221 days', u'Петросян', u'Питер', u'2292', 2),
    (u'Жаба за 3 дня', u'Сидоров', u'БХВ', u'1998', 3),
)


################################################################
db_is_new = not os.path.exists(db_filename)


with sqlite3.connect(db_filename,
                     detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES) as conn:
    if db_is_new:
        print 'Creating schema for %s' % db_filename
        with open(schema_filename, 'rt') as f:
            schema = f.read()
        conn.executescript(schema)
        conn.commit()
        cur = conn.cursor()
        print 'Inserting initial data'
        print 'Filling in categories'
        cur.executemany("INSERT INTO categories(title, href) VALUES(?,?)", categories)
        conn.commit()
        print 'Filling in books'
        cur.executemany("INSERT INTO books(title, author, publisher, year, category) VALUES(?,?,?,?,?)",
                        books)
        conn.commit()
    else:
        print 'Database exists, assume schema does, too.'
