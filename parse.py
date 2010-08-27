#!/usr/bin/env python
# -*- coding: utf-8 -*-

import __future__
from urllib2 import urlopen, URLError
import re
import sys


def parse_pizzerias():
    # try:
    pizzerias_src = urlopen('http://onlinepizza.se/Linkoping/').read().decode('latin-1')
    # except URLError:
    #     #oops
    #     pass
    # except:
    #     pass

    pizzerias = [];

    pizzeria_expr = re.compile('printPizzeriaListItem(?:Premium)?\((?P<args>.*?\')\);')
    category_expr = re.compile('(?P<name>[^<]+)</a>')
    item_expr = re.compile('(?<!hintsKategorier)print[^ ]+Variant\((?P<data>[^;]+)\);')
    html_strip_expr = re.compile('<[^>]*>')

    pizzeria_iter = pizzeria_expr.finditer(pizzerias_src)
    for pizzeria_match in pizzeria_iter:
        args = pizzeria_match.group('args').split(',')
        pizzeria_url = args[3].strip('\' ')
        pizzeria_name = args[14].strip('\' ')
        pizzeria_id = args[2].strip('\' ')
        
        if pizzeria_id != '1999': #skip demo restaurant
            print(pizzeria_id)
            #try:
            print('http://onlinepizza.se/menyer/%s_onlinepizza.se_UtkorPris_java.js' % pizzeria_id)
            pizzeria_src = urlopen('http://onlinepizza.se/menyer/%s_onlinepizza.se_UtkorPris_java.js' % pizzeria_id).read().decode('latin-1')
            #except URLError:
            #    continue

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
                    data = item.group('data')
                    data = html_strip_expr.sub('', data)
                    category.items.append(eval(data))

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
                print piv[6]

if __name__ == '__main__':
    main()
