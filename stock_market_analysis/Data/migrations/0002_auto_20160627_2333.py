# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-28 03:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='daydata',
            name='close',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='daydata',
            name='high',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='daydata',
            name='low',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='daydata',
            name='open',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='daydata',
            name='volume',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
