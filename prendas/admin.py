# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Prendas

# Register your models here.

@admin.register(Prendas)

class Prendas(admin.ModelAdmin):
    '''
        Admin View for Prendas'''
    list_display = ('nombre_prenda', 'no_prendas')
    list_filter = ('nombre_prenda',)
    

