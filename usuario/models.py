# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser

from django.db import models

# Create your models here.

class User(AbstractUser):
	"""docstring for User"""
	no_empleado = models.CharField(max_length = 40)
	rfc = models.CharField(max_length = 15)
	edad = models.IntegerField(blank = True, null = True)
	puesto = models.CharField(max_length = 200)
	telefono = models.CharField(max_length = 10)

	class Meta:
		db_table = 'auth_user'

	def __str__(self):
		return self.no_empleado
