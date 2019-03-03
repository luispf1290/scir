# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import User

# Register your models here.

@admin.register(User)

class User(admin.ModelAdmin):
    '''
        Admin View for User'''
    list_display = ('no_empleado', 'rfc', 'edad', 'puesto', 'telefono', 'username')
    list_filter = ('username',)