# -*- coding: utf-8 -*-
#
################################################################################
# see: http://eax.me/pytest/
#
#
#
import os.path
import importlib.util
import pytest

path = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    '..',
                                    'fibgen',
                                    'fibgen.py'))
spec = importlib.util.spec_from_file_location('fibgen', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
# module.fibgen(3)


class TestFibgen:

    def test_type_error(self):
        with pytest.raises(TypeError):
            list(module.fibgen('ololo'))

    def test_negative(self):
        assert(list(module.fibgen(-1)) == [])

    def test_empty(self):
        assert(list(module.fibgen(0)) == [])

    def test_one(self):
        assert(list(module.fibgen(1)) == [1])

    def test_two(self):
        assert(list(module.fibgen(2)) == [1,1])

    def test_three(self):
        assert(list(module.fibgen(3)) == [1, 1, 2])

    def test_seven(self):
        # result = list(module.fibgen(10))
        result = list(module.fibgen(7))
        expected = [1, 1, 2, 3, 5, 8, 13]
        assert(result == expected)

    # @pytest.mark.randomize(num=int, min_num=3, max_num=1000, ncalls=100)
    # def test_quickcheck(self, num):
        # result = list(fibgen(num))
        # assert(result[0] < result[-1])
        # assert(len(result) == num)
