# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-09 02:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0004_auto_20170809_0239'),
    ]

    operations = [
        migrations.AddField(
            model_name='set',
            name='Level',
            field=models.IntegerField(default=0),
        ),
    ]