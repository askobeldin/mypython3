# -*- coding: utf-8 -*-
############################################################
# code based on book: Fluent python
# https://github.com/fluentpython/example-code
#
# Chapter: 7

def make_averager():
    count = 0
    total = 0

    def averager(new_value):
        nonlocal count, total
        count += 1
        total += new_value
        return total / count
    return averager


avg = make_averager()

for i in range(1, 100):
    print(avg(i))

