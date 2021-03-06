# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-08 02:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Data', '0012_auto_20160705_1518'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('type', models.IntegerField(choices=[(0, b'long'), (1, b'short')])),
                ('complete', models.BooleanField(default=False)),
                ('stop_loss', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('target', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('initial_price', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('start_price', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('start_date', models.DateField()),
                ('end_price', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Data.Stock')),
            ],
        ),
    ]
