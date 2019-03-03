# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Insumos(models.Model):

    class Meta:
        verbose_name = "Insumos"
        verbose_name_plural = "Insumos"

    nombre = models.CharField(max_length = 150)
    empresa = models.CharField(max_length = 150)
    uso = models.CharField(max_length= 350)
    unidades = models.IntegerField()
    presentacion = models.IntegerField()
    total = models.IntegerField()

    def __str__(self):
        return self.nombre
    