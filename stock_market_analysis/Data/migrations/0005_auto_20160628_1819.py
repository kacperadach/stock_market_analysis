# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 22:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0004_auto_20160628_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='daydata',
            name='average_volume',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='industry',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='stock',
            name='market_cap',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]