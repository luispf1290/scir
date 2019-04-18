# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Mantenimiento(models.Model):


    class Meta:
        verbose_name = "Mantenimiento"
        verbose_name_plural = "Mantenimientos"

    fecha = models.DateField(auto_now=False)
    descripcion = models.CharField(max_length=300)
    aplicado = models.BooleanField(default=False)

    def __str__(self):
        return self.descripcion
