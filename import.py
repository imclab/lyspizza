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
            Item(pizzeria = p_obj, category = cat_obj, name = pizza['name'],
                 number = pizza['listNum'], onlinepizza_id = pizza['id'])

        cat_index += 1
