# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
import datetime
from django.contrib.auth.models import User, Group


# class UserStripe(models.Model):
# 	user = models.OneToOneField(User)
	# stipe_id = models.CharField(max_length=120, null=True, blank=True)

class Video(models.Model):
	Tags = models.CharField(default = "", max_length=300)
	Title = models.CharField(default = "", max_length=200)
	File = models.FileField(upload_to='static/videos/', max_length=100)
	Thumbnail = models.FileField(upload_to='static/videos/Thumbnails', max_length=100)
	Exercise_Type = models.CharField(default="", max_length=200)
	Description = models.CharField(default="", max_length=1000)
	# Image = models.ImageField(upload_to='static/videos/Thumbnails', max_length=100)

class Member(models.Model):
	User = models.OneToOneField(User)
	Level = models.IntegerField(default=0)
	Stripe_ID = models.CharField(max_length=120, null=True, blank=True)
	Stripe_Created = models.BooleanField(default=False)
	# UBV_Push_Level = models.IntegerField(default=0)
	# UBH_Pull_Level = models.IntegerField(default=0)
	# UBV_Pull_Level = models.IntegerField(default=0)
	# LBU_Push_Level = models.IntegerField(default=0)
	# Ant_Chain_Level = models.IntegerField(default=0)
	# Post_Chain_Level = models.IntegerField(default=0)
	# Iso_1_Level = models.IntegerField(default=0)
	# Iso_2_Level = models.IntegerField(default=0)
	# Iso_3_Level = models.IntegerField(default=0)
	# Iso_4_Level = models.IntegerField(default=0)
	# RFD_Load_Level = models.IntegerField(default=0)
	# RFD_Unload_1_Level = models.IntegerField(default=0)
	# RFD_Unload_2_Level = models.IntegerField(default=0)
	# Med_Ball_Level = models.IntegerField(default=0)

	# Type = models.CharField(default="", max_length=200)
	# Level = models.IntegerField(default=0)
	# SignUp_Day = models.DateTimeField(auto_now=True)
	# Start_Date = models.DateTimeField()
	# Workout_Days = models.CharField(default="", max_length=5)

class Exercise(models.Model):
	# ID = models.CharField(default="", max_length=20)
	Video = models.ForeignKey(Video, blank=True, null=True, related_name="exercises")
	Video_Description = models.CharField(default="", max_length = 1000)
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
	Set_1 = models.CharField(default="", max_length=10)
	Set_2 = models.CharField(default="", max_length=10)
	Set_3 = models.CharField(default="", max_length=10)
	Set_4 = models.CharField(default="", max_length=10)

class Workout_Template(models.Model):
	Level_Group = models.IntegerField(default=0)
	Level = models.IntegerField(default=0)
	Ordered_ID = models.IntegerField(default=0)
	Week = models.IntegerField(default=0)
	Day = models.IntegerField(default=0)
	SubWorkouts = models.ManyToManyField(SubWorkout, default="")
	_Date = models.CharField(default="", max_length=10)
	Block_Num = models.IntegerField(default=0)
	Block = models.CharField(default="", max_length=200)

class Workout(models.Model):
	Member = models.ForeignKey(Member, related_name="workouts")
	Template = models.ForeignKey(Workout_Template)
	Level = models.IntegerField(default=0)
	Ordered_ID = models.IntegerField(default=0)
	Week = models.IntegerField(default=0)
	Day = models.IntegerField(default=0)
	Sets = models.ManyToManyField(Set, default="", null=True, blank=True)
	Date = models.DateField()
	_Date = models.CharField(default="", max_length=10)
	SubWorkouts = models.ManyToManyField(SubWorkout, default="")
	_User = models.OneToOneField(User, null=True)

