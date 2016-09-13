# -*- coding: utf-8 -*-
#
################################################################################
# see: http://eax.me/pytest/
#
#
#
import sys
import os

# ???
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest


def test_a():
    with pytest.raises(AssertionError):
        assert 1 > 2


class TestB:
    def test_b(self):
        assert 'a'.upper() == 'A'

    def test_c(self):
        with pytest.raises(ZeroDivisionError):
            1/0

