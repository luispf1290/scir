# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Prendas(models.Model):

    class Meta:
        verbose_name = "Prendas"
        verbose_name_plural = "Prendas"
        
    nombre_prenda = models.CharField(max_length = 255)
    no_prendas = models.IntegerField()
    
    def __str__(self):
        return self.nombre_prenda
    