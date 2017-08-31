# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-08-28 19:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Users', '0003_auto_20170820_1951'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Tags', models.CharField(default='', max_length=300)),
                ('Title', models.CharField(default='', max_length=200)),
                ('File', models.FileField(upload_to=None)),
            ],
        ),
    ]
