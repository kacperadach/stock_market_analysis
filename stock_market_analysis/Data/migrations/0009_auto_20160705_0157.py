# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-05 05:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0008_auto_20160703_1407'),
    ]

    operations = [
        migrations.AddField(
            model_name='advancedstats',
            name='fourteen_day_ema_gain',
            field=models.DecimalField(blank=True, decimal_places=17, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='advancedstats',
            name='fourteen_day_ema_loss',
            field=models.DecimalField(blank=True, decimal_places=17, max_digits=20, null=True),
        ),
    ]
