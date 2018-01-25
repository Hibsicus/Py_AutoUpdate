# -*- coding: utf-8 -*-
from xml.etree.ElementTree import parse, Element, ElementTree


doc = parse('config.xml')
root = doc.getroot()


for elem in doc.iter(tag='version'):
    elem.text = '1.1.1.1'



doc.write('config1.xml', encoding='utf-8', xml_declaration=True)