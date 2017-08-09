# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Workout, Set, Exercise, Member
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import datetime, time

def Home(request):
	context = {}
	return render(request, "homepage.html", context)

def Member_Home(request):
	context = {}
	context["Sets"] = []
	context["Test"] = "Test context"
	anonymous = True
	user = request.user
	if (user.is_anonymous() == False): 
		Current_Workout = Workout.objects.get(_User = user, Date=datetime.date.today())
		anonymous = False
	count = 0
	if (anonymous == False):
		for i in Current_Workout.Sets.all():
			if i.Order == count + 1:
				row = []
				row.append(i.Exercise)
				row.append(i.Reps)
				row.append(i.Rest_Time)
				count += 1
				Context["Sets"].append(row)

	if(request.GET.get("form_test")):
		print("test form")
		return HttpResponseRedirect('/member-home/')

	if(request.GET.get("test_button")):
		print("test button")
		context["Test"] = "Test change"
		return render(request, "member_home.html", context)
	# new_user = User.objects.create(username=email, first_name=f_name, last_name=l_name, password=p_1)
	 # new_user.save()
	return render(request, "member_home.html", context)

def Admin(request):
	context = {}
	context["Users"] = []
	for i in Member.objects.all():
		row = []
		row.append(Member.pk)
		row.append(Member.User.first_name)
		row.append(Member.User.last_name)
		row.append(Member.User.email)
		row.append(Member.Level)
		context["Users"].append(row)
	return render(request, "admin.html", context)

