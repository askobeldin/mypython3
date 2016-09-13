# -*- coding: utf-8 -*-
#
################################################################################
# see: http://eax.me/pytest/
#
#
#
import sys
import os
import decimal

# ???
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest

from foo import summa


class TestSumma_func:

    def test_one(self):
        assert(summa('3.025e5', '4.147') == decimal.Decimal('302504.147'))
