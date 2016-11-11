#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
################################################################################
"""
Выводит на консоль содержимое xml файла для разбора человеком
"""
import xml.dom.minidom


# xml = xml.dom.minidom.parse(xml_fname) 
# or xml.dom.minidom.parseString(xml_string)

xml = xml.dom.minidom.parse("Rama1.jlx")
pretty_xml_as_string = xml.toprettyxml()
print(pretty_xml_as_string)
