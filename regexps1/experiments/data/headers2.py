# -*- coding: utf-8 -*-
#
###############################################################################
# looking for \n for different platforms --> (?:\n|\r|\r\n?)

# strings
h1 = '# This is header one.   '
h11 = '# This is header one.   ###### '
h2 = '#This is header two!!.'
h21 = '#This is header two #'
h3 = '# This is header, one and two.  '
h31 = '# This is header, one and two. # '


# regexps
r1 = r'^#{1}\s*(?P<value>\b.+\b)'
r2 = r'^#{1}\s*(?P<value>\b.+\b(?:\.|\!|\?)?)'

# main table for testing
# must be in every file
# third element in tuple - flags for compile: M, I, S
# in case of some flags = 'MIS'
retable = (
    (r'^#', h1),
    (r'^#{1}\s*', h1),
    (r1, h1),
    (r1, h11),

    (r1, h2),
    (r1, h21),

    (r2, h1),
    (r2, h11),
    (r2, h2),
    (r2, h21),

    (r2, h3),
    (r2, h31),
)

