# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 03:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0002_auto_20160627_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daydata',
            name='close',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='daydata',
            name='high',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='daydata',
            name='low',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='daydata',
            name='open',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=7, null=True),
        ),
    ]