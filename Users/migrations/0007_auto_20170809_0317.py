# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-09 03:17
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0006_auto_20170809_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='_User',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]