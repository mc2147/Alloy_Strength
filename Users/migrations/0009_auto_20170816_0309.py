# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-16 03:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0008_auto_20170816_0256'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='Exercise_Type',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='Type',
            field=models.CharField(default='', max_length=200),
        ),
    ]
