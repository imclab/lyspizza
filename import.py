#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import setup_environ
import settings
setup_environ(settings)
import sys

from lyspizza.main.models import *

from parse import parse_pizzerias

pizzerias = parse_pizzerias()

for p in pizzerias:
    p_obj = Pizzeria(name = p.name, url = p.url)
    p_obj.save()
    cat_index = 0
    print "\n-" + p.name
    for cat in p.categories:
        cat_obj = ItemCategory(name = cat.name, index = cat_index, pizzeria = p_obj)
        cat_obj.save()
        for pizza in cat.items:
            print ".",
            if len(pizza) == 10:
                Item(pizzeria = p_obj, category = cat_obj, name = pizza[6],
                     number = pizza[5], price = pizza[7],
                     ingredients = pizza[9], onlinepizza_id = pizza[4]).save()
            elif len(pizza) == 15:
                Item(pizzeria = p_obj, category = cat_obj, name = pizza[6],
                     number = pizza[5], price = pizza[11],
                     ingredients = pizza[7], onlinepizza_id = pizza[1]).save()
            else:
                print >> sys.stderr, "unknown data column number: %s" % (pizza)


        cat_index += 1
