# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-04-18 02:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mantenimiento',
            name='aplicado',
            field=models.BooleanField(default=False),
        ),
    ]
