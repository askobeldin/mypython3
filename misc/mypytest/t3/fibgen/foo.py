# -*- coding: utf-8 -*-
#
################################################################################
from decimal import Decimal, getcontext

def summa(a, b):
    da = Decimal(a)
    db = Decimal(b)
    return da + db
