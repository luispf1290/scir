# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Insumos

# Register your models here.

@admin.register(Insumos)
class Insumos(admin.ModelAdmin):
    '''
        Admin View for Insumos'''
    list_display = ('nombre', 'empresa', 'uso', 'unidades', 'presentacion')
    list_filter = ('nombre',)