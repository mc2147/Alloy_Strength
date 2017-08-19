# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import datetime
from django.contrib.auth.models import User, Group

class Member(models.Model):
	User = models.OneToOneField(User)
	Level = models.IntegerField(default=0)

class Exercise(models.Model):
	# ID = models.CharField(default="", max_length=20)
	New_Code = models.CharField(default="", max_length=20)
	Code = models.CharField(default="", max_length=20)
	Name = models.CharField(default="", max_length=200)
	Type = models.CharField(default="", max_length=200)
	Level = models.IntegerField(default=0)
	Bodyweight = models.BooleanField(default=False)

class Set(models.Model):
	Sets = models.IntegerField(default=0)
	Code = models.CharField(default="", max_length=2) # Level + Exercise Type
	Exercise = models.OneToOneField(Exercise, default="", null=True, blank=True)
	Exercise_Type = models.CharField(default="", max_length=200)
	Level = models.IntegerField(default=0)
	Reps = models.IntegerField(default=0)
	Rest_Time = models.DurationField(default=datetime.timedelta(minutes=2, seconds=0))
	Order = models.IntegerField(default=0)

class SubWorkout(models.Model):
	# Workout = models.OneToOneField(Workout, default="")
	# Exercise = models.OneToOneField(Exercise, default="", null=True, blank=True)
	Exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, blank=True, null=True)
	Exercise_Type = models.CharField(default="", max_length=200)
	Sets = models.IntegerField(default=0)
	Reps = models.IntegerField(default=0)
	Order = models.IntegerField(default=0)
	RPE = models.CharField(default="", max_length=3)
	Deload = models.IntegerField(default=0)
	Money = models.IntegerField(default=0)

class Workout_Template(models.Model):
	Level_Group = models.IntegerField(default=0)
	Level = models.IntegerField(default=0)
	Ordered_ID = models.IntegerField(default=0)
	Week = models.IntegerField(default=0)
	Day = models.IntegerField(default=0)
	SubWorkouts = models.ManyToManyField(SubWorkout, default="")
	_Date = models.CharField(default="", max_length=10)

class Workout(models.Model):
	Template = models.ForeignKey(Workout_Template)
	Level = models.IntegerField(default=0)
	Ordered_ID = models.IntegerField(default=0)
	Week = models.IntegerField(default=0)
	Day = models.IntegerField(default=0)
	Sets = models.ManyToManyField(Set, default="", null=True, blank=True)
	Date = models.DateField(auto_now=True)
	_Date = models.CharField(default="", max_length=10)
	SubWorkouts = models.ManyToManyField(SubWorkout, default="")
	# _User = models.OneToOneField(User, null=True)

