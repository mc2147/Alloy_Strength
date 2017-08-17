# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Workout, Set, Exercise, Member, SubWorkout
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, time

Exercise_Types = ["UB Hor Push", "UB Vert Push",  "UB Hor Pull", "UB Vert Pull",  "Hinge", "Squat", "LB Uni Push", 
"Ant Chain", "Post Chain",  "Isolation", "Iso 2", "Iso 3", "Iso 4", "RFL Load", "RFD Unload 1", "RFD Unload 2"]

def User_Page(request): 
	test_var = "" 
	return render(request, "userpage.html", {'test_var': test_var})

Days_Of_Week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def Generate_Workouts(Start_Date, Level, Days_List):
	Days = enumerate(Days_List)
	Workouts = Workout_Templates.objects.get(Level=Level)
	if Level <= 5:
		# Create workout objects with dates according to the next 4 weeks
		# 1. Get day of the week of start_date (should be one of Days_List)
		# 	Give member option to choose one of the 3-4 Days to start on
		# 2. Get all workout days...
		# Order the workouts
		count = 0
		for i in range(1, 29): #i will be from 1 to 28
			if (Start_Date + timedelta(days=i)).weekday() in Days:
				count += 1
				string_date = Start_Date.strftime('%m/%d/%Y')
				_Template = Workout_Templates.objects.get(Level=Level, Ordered_ID = count)
				_Workout = Workout(Template=_Template, _Date=string_date)
				_Workout.save()
				print(Start_Date.strftime('%m/%d/%Y'))

			# .weekday(timedelta(days=i+1))





@csrf_exempt 
def Workout_Update(request): 
	if request.method == 'POST': 
		if 'TempDate' in request.POST: 

			# test_var = date 
			test_var = request.POST['TempDate']
			print "Request is", request 
			print test_var
			print isinstance(test_var, basestring)

			if (Workout.objects.filter(_Date=test_var)).exists():
				_Workout = Workout.objects.get(_Date=test_var)
				print("Workout Level: " + str(_Workout.Level))
				_Level = _Workout.Level
				_Exercise_Name = _Workout.SubWorkouts.all()[0].Exercise.Name

			# Include Model filtering here based on test_var
		
			# Only for one row 
			return JsonResponse({
				'status': 'success',
				'pattern': 'pattern:' + test_var,
				'level': str(_Level), 
				'exercise': _Exercise_Name, 
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

	context["Exercise_Types"] = Exercise_Types
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
		# row.append(i.Exercise.Name)
		row.append(i.Reps)
		row.append(i.Code)
		context["Sets"].append(row)
	for i in Workout.objects.all():
		row = []
		sets = ""
		row.append(i.Level)
		row.append(i.Week)
		row.append(i.Day)
		for x in i.SubWorkouts.all():
			# _type = x.Exercise_Type
			# _level = x.Level
			# print(_type)
			# print(_level)
			# _exercise = Exercise.objects.get(Type = _type, Level = _level)
			# x.Exercise = _exercise
			# x.save()
			sets = sets + x.Exercise.Name + " " + str(x.Sets) + " x " + str(x.Reps) + ", "
		row.append(sets)
		context["Workouts"].append(row)

	if(request.GET.get("delete_all")):
		Member.objects.all().delete()
		Exercise.objects.all().delete()
		Set.objects.all().delete()
		Workout.objects.all().delete()
		SubWorkout.objects.all().delete()
		return HttpResponseRedirect("/admin-site")

	if(request.GET.get("delete_sets_workouts")):
		Set.objects.all().delete()
		Workout.objects.all().delete()
		return HttpResponseRedirect("/admin-site")

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
		set_exercise_type = request.GET.get("set_type")
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
  		w_date = request.GET.get("workout_date")
		_workout = Workout(Level = w_level, Week = w_week, Day = w_day, _Date = w_date)
		_workout.save()

		Exercise_1_Type = request.GET.get("workout_set_1_type")
		Exercise_1_Sets = request.GET.get("workout_set_1_num")
		Exercise_1_Reps = request.GET.get("workout_set_1_reps")

		if Exercise_1_Sets != "" and Exercise_1_Reps != "":
			print(Exercise_1_Type)
			print(Exercise_1_Sets)
			print(Exercise_1_Reps)
			Sub_1_Exercise = Exercise.objects.get(Level=w_level, Type=Exercise_1_Type)
			print(Sub_1_Exercise.Name)
			Sub_1 = SubWorkout(Sets = Exercise_1_Sets, Reps = Exercise_1_Reps)
			Sub_1.Exercise = Sub_1_Exercise
			Sub_1.save()
			_workout.SubWorkouts.add(Sub_1)
			_workout.save()


		# Exercise_2_Type = request.GET.get("workout_set_2_type")
		# Exercise_2_Sets = request.GET.get("workout_set_2_num")
		# Exercise_2_Reps = request.GET.get("workout_set_2_reps")

		# if Exercise_2_Sets != "" and Exercise_2_Reps != "":

		# Exercise_3_Type = request.GET.get("workout_set_3_type")
		# Exercise_3_Sets = request.GET.get("workout_set_3_num")
		# Exercise_3_Reps = request.GET.get("workout_set_3_reps")

		# if Exercise_3_Sets != "" and Exercise_3_Reps != "":

		# Exercise_4_Type = request.GET.get("workout_set_4_type")
		# Exercise_4_Sets = request.GET.get("workout_set_4_num")
		# Exercise_4_Reps = request.GET.get("workout_set_4_reps")

		# if Exercise_4_Sets != "" and Exercise_4_Reps != "":

		# Exercise_5_Type = request.GET.get("workout_set_5_type")
		# Exercise_5_Sets = request.GET.get("workout_set_5_num")
		# Exercise_5_Reps = request.GET.get("workout_set_5_reps")

		# if Exercise_5_Sets != "" and Exercise_5_Reps != "":

		# Exercise_6_Type = request.GET.get("workout_set_6_type")
		# Exercise_6_Sets = request.GET.get("workout_set_6_num")
		# Exercise_6_Reps = request.GET.get("workout_set_6_reps")

		# if Exercise_6_Sets != "" and Exercise_6_Reps != "":



  		# w_set_1 = Set.objects.get(Code = request.GET.get("workout_set_1_code"))

  		# set_1_exercise = Exercise.objects.get_or_create(Level=w_level, Type=request.GET.get("workout_set_1_type"))
  		# set_1_exercise.save()
  		# print(request.GET.get("workout_set_1_type"))
  	
  	# 	if Exercise.objects.filter(Level=w_level, Type=request.GET.get("workout_set_1_type")).exists():
  	# 		print("Exists")
	  # 		set_1_exercise = Exercise.objects.get(Level=w_level, Type=request.GET.get("workout_set_1_type"))
	  # 		set_1_exercise.save()
	  # 		print(set_1_exercise.Type)
	  # 		w_set_1 = Set(Code = w_level, Level=w_level, 
	  # 		Reps=request.GET.get("workout_set_1_reps"), Exercise_Type=request.GET.get("workout_set_1_type"))
	  # 		w_set_1.save()
	  # 		# w_set_1.Exercise = set_1_exercise
			# _workout.Sets.add(w_set_1)

  	# 	if request.GET.get("workout_set_2_reps") != "":
	  # 		set_2_exercise = Exercise.objects.get(Level=w_level, Type=request.GET.get("workout_set_2_type"))
	  # 		set_2_exercise.save()
	  # 		w_set_2 = Set(Code = w_level, Exercise = set_2_exercise, Level=w_level, Reps=request.GET.get("workout_set_2_reps"))
	  # 		w_set_2.save()
			# _workout.Sets.add(w_set_2)
  	# 	if request.GET.get("workout_set_3_code") != "":
	  # 		set_3_exercise = Exercise.objects.get(Level=w_level, Type=request.GET.get("workout_set_3_type"))
	  # 		w_set_3 = Set(Code = w_level, Exercise = set_3_exercise, Level=w_level, Reps=request.GET.get("workout_set_3_reps"))
	  # 		w_set_3.save()
			# _workout.Sets.add(w_set_3)
  	# 	if request.GET.get("workout_set_4_code") != "":
	  # 		set_4_exercise = Exercise.objects.get(Level=w_level, Type=request.GET.get("workout_set_4_type"))
	  # 		w_set_4 = Set(Code = w_level, Exercise = set_4_exercise, Level=w_level, Reps=request.GET.get("workout_set_4_reps"))
	  # 		w_set_4.save()
			# _workout.Sets.add(w_set_4)
  	# 	if request.GET.get("workout_set_5_code") != "":
	  # 		set_5_exercise = Exercise.objects.get(Level=w_level, Type=request.GET.get("workout_set_5_type"))
	  # 		w_set_5 = Set(Code = w_level, Exercise = set_5_exercise, Level=w_level, Reps=request.GET.get("workout_set_5_reps"))
	  # 		w_set_5.save()
			# _workout.Sets.add(w_set_5)
  	# 	if request.GET.get("workout_set_6_code") != "":
	  # 		set_6_exercise = Exercise.objects.get(Level=w_level, Type=request.GET.get("workout_set_6_type"))
	  # 		w_set_6 = Set(Code = w_level, Exercise = set_6_exercise, Level=w_level, Reps=request.GET.get("workout_set_6_reps"))
	  # 		w_set_6.save()
			# _workout.Sets.add(w_set_6)

		# _workout.save()
		return HttpResponseRedirect("/admin-site")
		# return render(request, "admin.html", context)	
	return render(request, "admin.html", context)

