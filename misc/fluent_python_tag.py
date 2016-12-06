# -*- coding: utf-8 -*-
###############################################################################
# Fluent python book
#
# code example: 5.10

def tag(name, *content, cls=None, **attrs):
    """Генерирует один или несколько HTML тегов"""
    if cls is not None:
        attrs['class'] = cls
    if attrs:
        attr_str = ''.join(' %s="%s"' % (attr, value)
                           for attr, value
                           in sorted(attrs.items()))
    else:
        attr_str = ''
    if content:
        return '\n'.join('<%s%s>%s</%s>' %
                         (name, attr_str, c, name) for c in content)
    else:
        return '<%s%s />' % (name, attr_str)



# testing
print(tag('br'))
print(tag('p', 'hello'))
print(tag('p', 'hello', 'world'))

print(tag('p', 'hello', id=33))
print(tag('p', 'hello', 'world', cls='sidebar'))
print(tag(content='testing', name='img'))

###############################
#  <br />
#  <p>hello</p>
#  <p>hello</p>
#  <p>world</p>
#  <p id="33">hello</p>
#  <p class="sidebar">hello</p>
#  <p class="sidebar">world</p>
#  <img content="testing" />
