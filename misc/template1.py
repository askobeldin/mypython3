# -*- coding: utf-8 -*-
#
################################################################################
from string import Template

s = Template('$who likes $what')
s2 = Template('${noun}ification')

print(s.substitute(who='Tim', what='eggs'))
print(s2.substitute(noun='make'))
print('s2.template is {}'.format(s2.template))
