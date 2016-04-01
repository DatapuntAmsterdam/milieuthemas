# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-16 14:01
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('risicozones_bedrijven', '0006_bron'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bedrijf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('bedrijfsnaam', models.CharField(max_length=64, null=True)),
                ('adres', models.CharField(max_length=100, null=True)),
                ('stadsdeel', models.CharField(max_length=16, null=True)),
                ('aantal_bronnen', models.PositiveSmallIntegerField(null=True)),
                ('bevoegd_gezag', models.CharField(max_length=32, null=True)),
                ('categorie_bevi', models.CharField(max_length=100, null=True)),
                ('type_bedrijf', models.CharField(max_length=100, null=True)),
                ('opmerkingen', models.TextField(null=True)),
                ('geometrie_polygon', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=28992)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
