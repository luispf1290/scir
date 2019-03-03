# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-02-17 21:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('area', '0001_initial'),
        ('prendas', '0002_auto_20190217_2029'),
    ]

    operations = [
        migrations.CreateModel(
            name='Integral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folio', models.CharField(max_length=150)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('fk_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='area.Area')),
            ],
            options={
                'verbose_name': 'Integral',
                'verbose_name_plural': 'Integrals',
            },
        ),
        migrations.CreateModel(
            name='Recoleccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recolecccion', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Recoleccion',
                'verbose_name_plural': 'Recolecciones',
            },
        ),
        migrations.CreateModel(
            name='Solicitud',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recibe_serv', models.IntegerField(default='0')),
                ('recibe_lav', models.IntegerField(default='0')),
                ('total_serv', models.IntegerField(default='0')),
                ('total_lav', models.IntegerField(default='0')),
                ('fk_integral', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solicitud.Integral')),
                ('fk_prenda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prendas.Prendas')),
            ],
            options={
                'verbose_name': 'Solicitud',
                'verbose_name_plural': 'Solicitudes',
            },
        ),
        migrations.CreateModel(
            name='Turno',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turno', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Turno',
                'verbose_name_plural': 'Turnos',
            },
        ),
        migrations.AddField(
            model_name='integral',
            name='fk_recol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solicitud.Recoleccion'),
        ),
        migrations.AddField(
            model_name='integral',
            name='fk_turno',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='solicitud.Turno'),
        ),
    ]
