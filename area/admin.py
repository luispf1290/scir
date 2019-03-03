# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Area

# Register your models here.

@admin.register(Area)

class Area(admin.ModelAdmin):
    '''
        Admin View for Area'''
    list_display = ('codigo', 'nombre_area', 'stock')
    list_filter = ('codigo',)
   