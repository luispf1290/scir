# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-02-17 21:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Insumos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150)),
                ('empresa', models.CharField(max_length=150)),
                ('uso', models.CharField(max_length=350)),
                ('unidades', models.IntegerField()),
                ('presentacion', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Insumos',
                'verbose_name_plural': 'Insumos',
            },
        ),
    ]
