# -*- coding: utf-8 -*-
#
################################################################################
"""
Try to improve my info about importing

"""

import sys
import saa.utils

print('saa.REGISTRY is', saa.REGISTRY)
saa.utils.util1('test epta')
saa.utils.util1('а тут по-русски')
print('sys.path is:{}'.format('\n'.join(sys.path)))
