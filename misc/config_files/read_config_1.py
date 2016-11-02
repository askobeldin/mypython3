# -*- coding: utf-8 -*-
#
################################################################################
from configparser import ConfigParser, ExtendedInterpolation
import re
import myutils

parser = ConfigParser(interpolation=ExtendedInterpolation(), strict=True)
parser.SECTCRE = re.compile(r"\[ *(?P<header>[^]]+?) *\]")

with open('config1.cfg', encoding='utf-8') as f:
    parser.read_file(f)
    myutils.showconfig1(parser)
