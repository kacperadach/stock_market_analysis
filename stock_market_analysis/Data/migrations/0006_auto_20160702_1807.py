# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-02 22:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0005_auto_20160702_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advancedstats',
            name='fifty_day_ema',
            field=models.DecimalField(blank=True, decimal_places=17, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='advancedstats',
            name='ten_day_ema',
            field=models.DecimalField(blank=True, decimal_places=17, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='advancedstats',
            name='twenty_day_ema',
            field=models.DecimalField(blank=True, decimal_places=17, max_digits=20, null=True),
        ),
    ]
