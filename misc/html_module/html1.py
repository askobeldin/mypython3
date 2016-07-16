# -*- coding: utf-8 -*-
############################################################
import html


fmt = "{name:<32} {value:<16} {code:<16}"
hdict = html.entities.html5

for name in sorted(hdict):
    value=html.entities.html5[name]
    code = ', '.join([hex(ord(c)) for c in value])
    print(fmt.format(name=name,
                     value=value,
                     code=code))
