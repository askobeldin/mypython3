# -*- coding: utf-8 -*-
################################################################################
# PyCon 2016
# info from site: https://speakerdeck.com/pycon2016
#
#
def valid_term(term):
    words = term.split()
    exclusion_rules = (
        any(len(word) > 15 for word in words),
        len(words) > 5,
        any(c in term for c in ",!?:1234567890"),
        sum(ord(c) > 255 for c in term) > 2,
        all(len(word) < 3 for word in words)
    )
    return not any(exclusion_rules)


print(valid_term("this is a simple text"))
