# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.contrib.auth.models import User, Group

class Member(models.Model):
	User = models.OneToOneField(User)
	Level = models.IntegerField(default=0)

class Exercise(models.Model):
	Name = models.CharField(default="", max_length=200)
	Type = models.CharField(default="", max_length=1)
	Level = models.IntegerField(default=0)

class Set(models.Model):
	Code = models.CharField(default="", max_length=2) # Level + Exercise Type
	Exercise = models.OneToOneField(Exercise, default="", null=True, blank=True)
	Level = models.IntegerField(default=0)
	Reps = models.IntegerField(default=0)
	Rest_Time = models.DurationField(default=datetime.timedelta(minutes=2, seconds=0))
	Order = models.IntegerField(default=0)

class Workout(models.Model):
	Level = models.IntegerField(default=0)
	Week = models.IntegerField(default=0)
	Day = models.IntegerField(default=0)
	Sets = models.ManyToManyField(Set, default="", null=True, blank=True)
	Date = models.DateField(auto_now=True)
	_User = models.OneToOneField(User, null=True)
