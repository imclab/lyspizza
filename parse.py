#!/usr/bin/env python
# -*- coding: utf-8 -*-

import __future__
from urllib2 import urlopen, URLError
import re
import sys


def parse_pizzerias():
    pizzerias_src = urlopen('http://onlinepizza.se/Linkoping/').read().decode('utf-8')

    pizzerias = [];

    pizzeria_expr = re.compile('printPizzeriaListItem(?:Premium)?\((?P<args>.*?\')\);')
    category_expr = re.compile('(?P<name>[^<]+)</a>')
    item_expr = re.compile('(?<!hintsKategorier)print(?P<variant>Single|Multi)Variant\((?P<data>[^;]+)\);')
    html_strip_expr = re.compile('<[^>]*>')

    pizzeria_iter = pizzeria_expr.finditer(pizzerias_src)
    for pizzeria_match in pizzeria_iter:
        args = pizzeria_match.group('args').split(',')
        pizzeria_url = args[3].strip('\' ')
        pizzeria_name = args[14].strip('\' ')
        pizzeria_id = args[2].strip('\' ')
        
        if pizzeria_id != '1999': #skip demo restaurant
            pizzeria_src = urlopen('http://onlinepizza.se/menyer/%s_onlinepizza.se_UtkorPris_java.js' % pizzeria_id).read().decode('utf-8')

            pizzeria = Pizzeria(pizzeria_name, pizzeria_url)
            pizzerias.append(pizzeria)

            category_srcs = pizzeria_src.split('hintsKategorier.hide();">')

            for category_src in category_srcs[1:]:
                category_match = category_expr.match(category_src)
                if category_match == None:
                    continue

                category = Category(category_match.group('name'))
                pizzeria.categories.append(category)

                for item in item_expr.finditer(category_src):
                    rawdata = eval(html_strip_expr.sub('', item.group('data')))
                    data = {}

                    data['z-index'] = rawdata[0]
                    data['listNum'] = rawdata[5]
                    data['name'] = rawdata[6]

                    if item.group('variant') == 'Single':
                        data['multi'] = False
                        
                        data['hasRating'] = bool(rawdata[1])
                        data['ratingImage'] = rawdata[2]
                        data['rating'] = rawdata[3]
                        data['id'] = rawdata[4]

                        data['price'] = rawdata[7]
                        data['hasImage'] = bool(rawdata[8])
                        data['ingredients'] = rawdata[9]
                        data['specialType'] = rawdata[10]
                        data['unknown1'] = rawdata[11]
                        data['unknown2'] = rawdata[12]
                    else:
                        data['multi'] = True

                        data['id'] = rawdata[1]
                        data['hasRating'] = bool(rawdata[2])
                        data['ratingImage'] = rawdata[3]
                        data['rating'] = rawdata[4]

                        data['ingredients'] = rawdata[7]
                        data['ingredientInfoTop'] = rawdata[8]
                        data['ingredientInfoMargBottom'] = rawdata[9]
                        data['hasImage'] = bool(rawdata[10])
                        data['price'] = rawdata[11]
                        data['variants'] = rawdata[12]
                        data['variantPrices'] = rawdata[13]
                        data['variantIDs'] = rawdata[14]
                        data['unknown1'] = rawdata[15]
                        data['unknown2'] = rawdata[16]
                        
                    
                    category.items.append(data)

    return pizzerias

class Pizzeria:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.categories = []

class Category:
    def __init__(self, name):
        self.name = name
        self.items = []



def main():
    pizzerias = parse_pizzerias()

    for pv in pizzerias:
        print
        print
        print "--------------------"
        print "--------------------"
        print pv.name
        print pv.url
        print "--------------------"
        print "--------------------"
        for cat in pv.categories:
            print
            print "--------------------"
            print cat.name
            print "--------------------"
            for piv in cat.items:
                print piv['name']

if __name__ == '__main__':
    main()
