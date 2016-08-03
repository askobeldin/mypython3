# -*- coding: utf-8 -*-
#
################################################################################
# looking for \n for different platforms --> (?:\n|\r|\r\n?)



h1 = '# This is header one'
h11 = 'This is header one.   \n==============='
h12 = h1 + '   #  '
h13 = '#   Test-driven development'

h2 = '## This is header two'
h21 = 'This is header two\n---------------'


# main table for testing
# must be in every file
# third element in tuple - flags for comile: M, I, S
# in case of some flags = 'MIS'
retable = (
    (r'#', h1),
    (r'#{1}\s', h1),
    (r'#{1}\s+(?P<text>\w+)', h1),
    (r'#{1}\s+(?P<text>.+)', h1),
    (r'#{1}\s+(?P<text>.+)', h1 + '  #    '),
    (r'#{1}\s+(?P<text>.+?)', h1 + '  #    '),
    (r'#{1}\s+(?P<text>.+\b)', h12),
    (r'#{1}\s+(?P<text>.+\b)', h13),
    (r'#{1}\s+(?P<text>.+\b)', h13 + '#'),
    (r'#{1}\s?(?P<text>.+\b)', '# Tesing header. #  '),
    (r'^#{1}\s?(?P<text>.+?\b)', '# Tesing header. #  '),
    (r'^#{1}\s?(?P<text>.+\b)', '#Tesing header.#  '),

    # semi-good for single line header
    (r'^#{1}\s?(?P<text>.+\b)', '# Tesing header 34. #  '),
    (r'^#{1}\s?(?P<text>.+\b)', '# Tesing header 35. #  '),
    (r'^#{1}\s?(?P<text>.+\b)', ' # Tesing header 36. #  '),

    # good for header on couple lines
    (r'(?P<text>\b.+\b)[\W\s]+(?:\n|\r|\r\n?)\=+', h11, 'M'),

    # (?m) - this is the flag M
    (r'(?m)(?P<text>\b.+\b)[\W\s]+(?:\n|\r|\r\n?)\=+', h11),

    (r'(?P<text>\b.+\b)[\W\s]+(?:\n|\r|\r\n?)\=+', h11 + '   ', 'M'),
    (r'(?P<text>\b.+\b)[\W\s]+(?:\n|\r|\r\n?)\=+', '3. ' + h11 + '   ', 'M'),

    (r'^[^\d\s\.](?P<text>\b.+\b)[\W\s]+(?:\n|\r|\r\n?)\=+', '3. ' + h11 + '   ', 'M'),
)

