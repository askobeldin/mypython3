# -*- coding: utf-8 -*-
#
################################################################################
import io
import string
from collections import namedtuple, deque



# Returns True if textline consist from the same symbols and length > 3 symbols
def isline(textline):
    st = textline.strip()
    return all((len(set(st)) == 1, len(st) > 3))

# Returns True if textline is empty
isempty = lambda textline: len(textline.strip()) == 0

Item = namedtuple('Item', 'kind value')
"""
    Item('EMPTY', '') - empty text line
    Item('LINE', '=') - text line consists from `=` symbols
    Item('TEXT', 'This is a text') - it is a text line
"""

# def textlineinfo(textline):
    # """возвращает кортеж, описывающий некоторые параметры исследуемой
    # строки textline

    # shift - количество пробелов от начала строки до ее первого непробельного
    # символа
    # firstsymbol - первый непробельный символ в строке
    # """
    # firstsymbol = ''
    # shift = 0
    # for n, v in enumerate(textline):
        # if v in string.whitespace:
            # shift = n
            # continue
        # if v in string.punctuation:
            # shift = n
            # firstsymbol = v
            # break
        # if v.isalnum():
            # shift = n
            # firstsymbol = v
            # break
    # return shift, firstsymbol


def items(filename, encoding='utf-8'):
    with open(filename, 'r', encoding=encoding) as f:
        textlines = [line.expandtabs(4) for line in f.readlines()]
    for line in textlines:
        if isempty(line):
            yield Item(kind='EMPTY', value='')
        elif isline(line):
            yield Item(kind='LINE', value=set(line.strip()).pop())
        else:
            yield Item(kind='TEXT', value=line)

SWITCH_TABLE = ()

class MDConverter:
    def __init__(self, filename, encoding='utf-8'):
        self.textitems = items(filename, encoding)
        # state machine parameters
        self.lastitem = ''
        self.state = ''
        self.buffer = deque()

    def astextfile(self):
        """Returns as text file
        """
        with io.StringIO() as out:
            for i in self.textitems:
                print(i, file=out)
            return out.getvalue()


# def MDConverter(filename, encoding='utf-8'):
    # # init
    # textitems = items(filename, encoding)
    # # state machine parameters
    # lastitem = ''
    # state = ''
    # machinebuffer = deque()
    # # processing
    # with io.StringIO() as output:
        # for item in textitems:


