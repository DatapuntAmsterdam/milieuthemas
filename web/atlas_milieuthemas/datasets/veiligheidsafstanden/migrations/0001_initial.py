# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-10 09:44
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('themas', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Veiligheidsafstand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('geo_id', models.IntegerField()),
                ('type', models.CharField(max_length=100, null=True)),
                ('locatie', models.CharField(max_length=100, null=True)),
                ('geometrie_multipolygon', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=28992)),
                ('geometrie_point', django.contrib.gis.db.models.fields.PointField(null=True, srid=28992)),
                ('thema', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='themas.Thema')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
