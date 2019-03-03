# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import Recoleccion, Solicitud, Turno

# Register your models here.
@admin.register(Recoleccion)

class Recoleccion(admin.ModelAdmin):
    '''
        Admin View for Recoleccion'''
    list_display = ('recolecccion',)
    list_filter = ('recolecccion',)

@admin.register(Turno)

class Turno(admin.ModelAdmin):
    '''
        Admin View for Turno'''
    list_display = ('turno',)
    list_filter = ('turno',)

# @admin.register(Solicitud)

# class Solicitud(admin.ModelAdmin):
#     '''
#         Admin View for Solicitud'''
#     list_display = ('folio', 'fecha', 'id_serv_area')
#     list_filter = ('folio',)