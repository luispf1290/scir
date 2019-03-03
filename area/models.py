# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Area(models.Model):

    class Meta:
        verbose_name = "Area"
        verbose_name_plural = "Areas"
        
    codigo = models.CharField(max_length = 8)
    nombre_area = models.CharField(max_length=255)
    stock = models.IntegerField()

    def __str__(self):
        return self.nombre_area
    