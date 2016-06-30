# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-29 23:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Data', '0006_auto_20160629_1808'),
    ]

    operations = [
        migrations.CreateModel(
            name='AdvancedStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rsi', models.IntegerField(blank=True, null=True)),
                ('data', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Data.DayData')),
            ],
        ),
        migrations.RemoveField(
            model_name='stock',
            name='industry',
        ),
        migrations.AddField(
            model_name='stock',
            name='eps',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='pe',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='peg',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='stock',
            name='short_ratio',
            field=models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True),
        ),
    ]
