# -*- coding: utf-8 -*-
############################################################
"""
SM - конечный автомат, разбивает предложение при посимвольном чтении на слова
по пробелам и знакам пунктуации (их игнорирует)
"""

import string


SENTENCE = 'this is,a,test,sentence here, ептыть!!!'


isletter = lambda ch: ch.isalnum()
ispunct = lambda ch: ch in string.punctuation


class SM:
    def __init__(self):
        self.cur = ''
        self.buf = []
        self.state = 'R'
        self.container = []
    def process(self, ch):
        self.cur = ch
        if isletter(self.cur):
            self.setstate('C')
        if self.cur.isspace():
            self.setstate('R')
        if ispunct(self.cur):
            self.setstate('R')
    def setstate(self, ns):
        if ns == 'C':
            self.buf.append(self.cur)
            self.state = 'C'
            return
        else:
            # ns == R
            if self.state == 'C':
                # self.buf.append(self.cur)
                self.cur = ''
                self.state = 'R'
                self.container.append(''.join(self.buf))
                self.buf.clear()
                return
            if self.state == 'R':
                self.cur = ''
                return
    def aslist(self):
        return self.container



def main(s):
    a = SM()
    for i in s:
        a.process(i)
    print('{!r} divided on:\n{}'.format(s, a.aslist()))


if __name__ == '__main__':
    main(SENTENCE)

