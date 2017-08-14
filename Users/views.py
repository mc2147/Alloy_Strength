# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Workout, Set, Exercise, Member
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import datetime, time


def User_Page(request): 
	test_var = "" 
	return render(request, "userpage.html", {'test_var': test_var})


@csrf_exempt 
def Workout_Update(request): 
	if request.method == 'POST': 
		if 'TempDate' in request.POST: 

			# test_var = date 
			test_var = request.POST['TempDate']
			print "Request is", request 

			# Include Model filtering here based on test_var
		
			# Only for one row 
			return JsonResponse({
				'status': 'success',
				'pattern': 'pattern:' + test_var,
				'level': 'level: ' + test_var, 
				'exercise': 'exercise: ' + test_var, 
				'weight': 'weight: ' + test_var, 
				'rpe': 'rpe: ' + test_var, 
				'tempo': 'tempo: ' + test_var,
				})
		else: 
			return JsonResponse({'status': 'fail'})		

def Home(request):
	context = {}
	return render(request, "homepage.html", context)

def Test(request):
	context = {}
	return render(request, "test.html", context)

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
	context["Exercises"] = []
	context["Sets"] = []
	context["Workouts"] = []

	context["Member_Added"] = ""
	context["Exercise_Added"] = ""
	context["Set_Added"] = ""
	context["Workout_Added"] = ""

	for i in Member.objects.all():
		row = []
		row.append(i.pk)
		row.append(i.User.first_name)
		row.append(i.User.last_name)
		row.append(i.User.username)
		row.append(i.Level)
		context["Users"].append(row)
	for i in Exercise.objects.all():
		row = []
		row.append(i.Level)
		row.append(i.Name)
		row.append(i.Type)
		context["Exercises"].append(row)
	for i in Set.objects.all():
		row = []
		row.append(i.Level)
		row.append(i.Exercise.Name)
		row.append(i.Reps)
		row.append(i.Code)
		context["Sets"].append(row)
	for i in Workout.objects.all():
		row = []
		sets = ""
		row.append(i.Level)
		row.append(i.Week)
		row.append(i.Day)
		for x in i.Sets.all():
			sets = sets + x.Exercise.Name + " x " + str(x.Reps) + ", "
		row.append(sets)
		context["Workouts"].append(row)

	#ADDING MEMBERS 
	if(request.GET.get("submitaddmember")):
		context["Member_Added"] = "Member Added"
		fname = request.GET.get("fname")
		lname = request.GET.get("lname")
		username = request.GET.get("username")
		password = request.GET.get("password")
		level = request.GET.get("level")

		new_user = User.objects.create(username=username, first_name=fname, last_name=lname, password=password)
		new_user.set_password(password)
		new_user.is_active = True
		new_user.save()

		new_member = Member(User=new_user, Level=level)
		new_member.save()
		return HttpResponseRedirect("/admin-site")
	#ADDING EXERCISES 
	if(request.GET.get("submitaddexercise")):
		context["Exercise_Added"] = "Exercise Added"

		exercise_name = request.GET.get("exercise_name")
		exercise_type = request.GET.get("exercise_type")
		exercise_level = request.GET.get("exercise_level")

		if Exercise.objects.filter(Name=exercise_name).exists() == False:
			new_exercise = Exercise(Name=exercise_name, Type=exercise_type, Level=exercise_level)
			new_exercise.save()
		return HttpResponseRedirect("/admin-site")

	# #ADDING SETS 
	if(request.GET.get("submitaddset")):
		context["Set_Added"] = "Set Added"
		set_exercise_name = request.GET.get("set_exercise")
		set_exercise = Exercise.objects.get(Name = set_exercise_name)
		set_type = request.GET.get("set_type")
		set_level = request.GET.get("set_level")
		set_reps = request.GET.get("set_reps")
		# set_rest_seconds = request.GET.get("set_rest_time")
		set_order = request.GET.get("set_order")

		new_set = Set(Code = set_level + set_type, Exercise = set_exercise, Level = set_level,
		Reps=set_reps, Order=set_order)
		new_set.save()
		return HttpResponseRedirect("/admin-site")

	# #ADDING WORKOUTS 
	if(request.GET.get("submitaddworkout")):
		context["Workout_Added"] = "Workout Added"

  		w_level = request.GET.get("workout_level")
  		w_week = request.GET.get("workout_week")
  		w_day = request.GET.get("workout_day")

  		w_set_1 = Set.objects.get(Code = request.GET.get("workout_set_1_code"))
  		if Set.objects.filter(Code = request.GET.get("workout_set_2_code")).exists():
	  		w_set_2 = Set.objects.get(Code = request.GET.get("workout_set_2_code"))
  		if Set.objects.filter(Code = request.GET.get("workout_set_3_code")).exists():
	  		w_set_3 = Set.objects.get(Code = request.GET.get("workout_set_3_code"))
  		if Set.objects.filter(Code = request.GET.get("workout_set_4_code")).exists():
	  		w_set_4 = Set.objects.get(Code = request.GET.get("workout_set_4_code"))
  		if Set.objects.filter(Code = request.GET.get("workout_set_5_code")).exists():
	  		w_set_5 = Set.objects.get(Code = request.GET.get("workout_set_5_code"))
  		if Set.objects.filter(Code = request.GET.get("workout_set_6_code")).exists():
	  		w_set_6 = Set.objects.get(Code = request.GET.get("workout_set_6_code"))

		_workout = Workout(Level = w_level, Week = w_week, Day = w_day)
		_workout.save()
		_workout.Sets.add(w_set_1)
		_workout.save()
		return HttpResponseRedirect("/admin-site")
		# return render(request, "admin.html", context)	
	return render(request, "admin.html", context)

