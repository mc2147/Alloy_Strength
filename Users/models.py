# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import datetime
from django.utils import timezone
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User, Group

class Member(models.Model):
	User = models.OneToOneField(User)
	Level = models.IntegerField(default=0)
	# Password
	# Email

# Specific exercise as in 'All Levels'
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

# Row in each table in 'Program'
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

# One page in 'Program'
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

class Post(models.Model): 
	author = models.ForeignKey('auth.User')
	title = models.CharField(max_length = 200)
	text = models.TextField()
	created_date = models.DateTimeField(default = timezone.now)
	published_date = models.DateTimeField(blank = True, null = True)


class Blog_Post(models.Model):
	Title = models.CharField(max_length=200)
	Content = RichTextUploadingField()
	Date = models.DateTimeField(blank = True, null = True)

	def publish(self): 
		self.Date= timezone.now()
		self.save()

	def __str__(self): 
		return self.Title 


