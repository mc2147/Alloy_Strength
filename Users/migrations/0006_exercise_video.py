# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-29 01:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0005_auto_20170828_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='Video',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='Users.Video'),
        ),
    ]