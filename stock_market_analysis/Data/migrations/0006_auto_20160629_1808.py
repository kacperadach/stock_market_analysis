# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0005_auto_20160628_1819'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='daydata',
            name='average_volume',
        ),
        migrations.AddField(
            model_name='stock',
            name='average_volume',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]