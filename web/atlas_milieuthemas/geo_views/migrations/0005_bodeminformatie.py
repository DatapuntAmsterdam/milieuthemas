# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-02-17 08:15
# Python
from __future__ import unicode_literals
# Packages
from django.db import migrations
# Project
from geo_views import migrate


class Migration(migrations.Migration):

    dependencies = [
        ('geo_views', '0004_risicozones_bedrijven'),
        ('bodeminformatie', '0003_asbest'),
    ]

    operations = [
        migrate.ManageView(
            view_name="geo_bodeminformatie_grondmonster",
            sql="""SELECT id, eindoordeel, geometrie
                    FROM bodeminformatie_grondmonster
                    WHERE geometrie IS NOT NULL"""
        ),
        migrate.ManageView(
            view_name="geo_bodeminformatie_grondwatermonster",
            sql="""SELECT id, eindoordeel, geometrie
                    FROM bodeminformatie_grondwatermonster
                    WHERE geometrie IS NOT NULL"""
        ),
        migrate.ManageView(
            view_name="geo_bodeminformatie_asbest",
            sql="""SELECT id, concentratie, geometrie
                    FROM bodeminformatie_asbest
                    WHERE geometrie IS NOT NULL"""
        ),
    ]