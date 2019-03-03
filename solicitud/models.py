# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from area.models import Area
from prendas.models import Prendas
# Create your models here.

class Turno(models.Model):

    class Meta:
        verbose_name = "Turno"
        verbose_name_plural = "Turnos"

    turno = models.CharField(max_length = 50)

    def __str__(self):
        return self.turno

class Recoleccion(models.Model):

    class Meta:
        verbose_name = "Recoleccion"
        verbose_name_plural = "Recolecciones"

    recolecccion = models.CharField(max_length = 150)

    def __str__(self):
        return self.recolecccion

class Integral(models.Model):

    folio = models.CharField(max_length=150)
    fecha = models.DateField(auto_now_add=True)
    fk_turno = models.ForeignKey(Turno, on_delete=None)
    fk_recol = models.ForeignKey(Recoleccion, on_delete=None)
    fk_area = models.ForeignKey(Area, on_delete=None)

    class Meta:
        verbose_name = "Integral"
        verbose_name_plural = "Integrals"

    def __str__(self):
        return self.folio


class Solicitud(models.Model):

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"

    fk_integral = models.ForeignKey(Integral)
    fk_prenda = models.ForeignKey(Prendas)
    recibe_serv = models.IntegerField(default='0')
    recibe_lav = models.IntegerField(default='0')
    total_serv = models.IntegerField(default='0')
    total_lav = models.IntegerField(default='0')
    
    def __str__(self):
        pass
    
    
    