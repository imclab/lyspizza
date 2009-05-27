#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lyspizza.main.models import *
from django.contrib import admin

admin.site.register(Pizzeria)
admin.site.register(ItemCategory)
admin.site.register(Item)
admin.site.register(Occasion)
admin.site.register(Attendance)
