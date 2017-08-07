# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.contrib.auth.models import User, Group

class Exercise(models.Model):
	Level = models.IntegerField(default=0)

class Set(models.Model):
	Exercise = models.OneToOneField(Exercise, default="", null=True, blank=True)
	Reps = models.IntegerField(default=0)
	Rest_Time = models.DurationField(default=datetime.timedelta(minutes=2, seconds=0))
	Order = models.IntegerField(default=0)

class Workout(models.Model):
	Sets = models.ManyToManyField(Set, default="", null=True, blank=True)
	Date = models.DateField(auto_now=True)
