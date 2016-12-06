# -*- coding: utf-8 -*-
#
################################################################################
h1 = '# This is header one'
h11 = 'This is header one\n==============='
h2 = '## This is header two'


# main table for testing
# must be in every file
# third element in tuple - flags for compile: M, I, S
# in case of some flags = 'MIS'
retable = (
    (r'#', h1),
    (r'#{1}\s', h1),
    (r'(\w+) (\w+)', 'Hello world'),
    (r'(?P<first>\w+) (?P<second>\w+)', 'Hello world'),

    (r'^\=+', '==========='),
    (r'^aaa$^\=+', 'aaa\n===========', 'M'),
    # looking for \n for different platforms?
    (r'.+(?:\n|\r|\r\n?)\=+', 'aaa\n===========', 'M'),
    (r'(\w+)$^\=+', h11, 'M'),
    (r'^\=+', h11, 'M'),
    (r'^[\=]{3,}', h11, 'M'),
    (r'^\w*$^[\=]{3,}', h11, 'M'),

)

