# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Workout, Set, Exercise, Member, SubWorkout, Workout_Template
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, time, timedelta

Exercise_Types = ["UB Hor Push", "UB Vert Push",  "UB Hor Pull", "UB Vert Pull",  "Hinge", "Squat", "LB Uni Push", 
"Ant Chain", "Post Chain",  "Isolation", "Iso 2", "Iso 3", "Iso 4", "RFL Load", "RFD Unload 1", "RFD Unload 2"]

def User_Page(request): 
	test_var = "" 
	return render(request, "userpage.html", {'test_var': test_var})


def Videos(request): 
	return render(request, "videos.html")

# def Test(request):
# 	return render(request, "")


Days_Of_Week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def Generate_Workouts(Start_Date, Level, Days_List):
	Week_Days = enumerate(Days_Of_Week)
	Days = Days_List
	# Workouts = Workout_Template.objects.get(Level=Level)
	Output = []
	if Level <= 5:
		# Create workout objects with dates according to the next 4 weeks
		# 1. Get day of the week of start_date (should be one of Days_List)
		# 	Give member option to choose one of the 3-4 Days to start on
		# 2. Get all workout days...
		# Order the workouts
		count = 0
		for i in range(1, 29): #i will be from 1 to 28
			if (Start_Date + timedelta(days=i)).weekday() in Days:
				Workout_Date = Start_Date + timedelta(days=i)
				count += 1
				string_date = Workout_Date.strftime('%m/%d/%Y')
				# _Template = Workout_Template.objects.get(Level_Group=1, Ordered_ID = count)
				# _Workout = Workout(Template=_Template, _Date=string_date)
				# _Workout.save()
				print(Workout_Date.strftime('%m/%d/%Y'))
				Output.append(string_date)
		return(Output)
	elif Level >= 6 and Level <= 10:
		return None
	elif Level >= 11 and Level <= 15:
		return None
	elif Level >= 16 and Level <= 25:
		return None

			# .weekday(timedelta(days=i+1))

def Test(request):
	context = {}
	print(Generate_Workouts(datetime(2017, 8, 1), 1, [0, 2, 4]))
	return render(request, "test.html", context)





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

	context["Weeks"] = [["Week 1", "W1", 1, [[[], [], [], [], [], []], [[], [], [], [], [], []], [[], [], [], [], [], []]] ], 
	["Week 2", "W2", 2], 
	["Week 3", "W3", 3], 
	["Week 4", "W4", 4]]
	context["Days"] = [["Day 1", "D1", 1],
	["Day 2", "D2", 2],
	["Day 3", "D3", 3]]
	context["Sets_Per_Workout"] = [["Set 1", 1],
	["Set 2", 2],
	["Set 3", 3],
	["Set 4", 4],
	["Set 5", 5],
	["Set 6", 6],]

	context["Test_Dict"] = {"Test": "Dictionary Works"}

	context["Placeholders"] = [
	[[[], [], [], [], [], []], [[], [], [], [], [], []], [[], [], [], [], [], []]], 
	[[[], [], [], [], [], []], [[], [], [], [], [], []], [[], [], [], [], [], []]], 
	[[[], [], [], [], [], []], [[], [], [], [], [], []], [[], [], [], [], [], []]], 
	[[[], [], [], [], [], []], [[], [], [], [], [], []], [[], [], [], [], [], []]]]
	# Week - 0 to 3
	# Day - 0 to 2
	# Set - 0 to 5

	context["Workout_Templates"] = [
	["Week 1", [["Day 1", [[], [], [], [], [], []]], ["Day 2", [[], [], [], [], [], []]], ["Day 3", [[], [], [], [], [], []]]]], 
	["Week 2", [["Day 1", [[], [], [], [], [], []]], ["Day 2", [[], [], [], [], [], []]], ["Day 3", [[], [], [], [], [], []]]]], 
	["Week 3", [["Day 1", [[], [], [], [], [], []]], ["Day 2", [[], [], [], [], [], []]], ["Day 3", [[], [], [], [], [], []]]]], 
	["Week 4", [["Day 1", [[], [], [], [], [], []]], ["Day 2", [[], [], [], [], [], []]], ["Day 3", [[], [], [], [], [], []]]]]]

	for i in Workout_Template.objects.all():
		_week_index = i.Week - 1 #Workout_Templates[index]
		_day_index = i.Day - 1 #Workout_Templates[week][1][_day_index]		
		print("Existing Workout Template: " + "Week " + str(i.Week) + " Day " + str(i.Day) + " Ordered ID: " + str(i.Ordered_ID))
		for x in i.SubWorkouts.all():			
			_exercise_type = x.Exercise_Type
			_sets = x.Sets
			_reps = x.Reps			
			_order = x.Order
			print(x.Exercise_Type + " " + str(x.Sets) + " x " + str(x.Reps)) + " (Set " + str(x.Order) + ")"
			_subworkout_index = x.Order - 1
			context["Workout_Templates"][_week_index][1][_day_index][1][_subworkout_index] = [_exercise_type, str(_sets) + " x ", _reps, "Set " + str(_order) + ":"]

	for i in context["Weeks"]:
		for y in context["Days"]:
			btn_code = i[1] + y[1] + "_Update_Workout"
			_week = i[2]
			_day = y[2]
			if Workout_Template.objects.filter(Level_Group=1, Week=_week, Day=_day).exists() == False:
				print("Created Workout Template: " + str(_week) + str(_day))
				_Workout_Template = Workout_Template(Level_Group=1, Week=_week, Day=_day)
				_Workout_Template.Ordered_ID = (_week - 1)*3 + _day
				_Workout_Template.save()
			else:
				_Workout_Template = Workout_Template.objects.get(Level_Group=1, Week=_week, Day=_day)
				_Workout_Template.Ordered_ID = (_week - 1)*3 + _day
				_Workout_Template.save()

			if request.GET.get(btn_code):
				print(btn_code)
				for z in range(1,7):
					if (_Workout_Template.SubWorkouts.all().filter(Order = z).exists()):
						_Placeholder_SubWorkout = _Workout_Template.SubWorkouts.all().get(Order = z)
						
						_Type = _Placeholder_SubWorkout.Exercise_Type
						_Sets = _Placeholder_SubWorkout.Sets
						_Reps = _Placeholder_SubWorkout.Reps
						# context["Placeholders"][_week - 1][_day - 1][z - 1] = [_Type, _Sets, _Reps]

					_sets = "Sets_" + str(z)
					_reps = "Reps_" + str(z)
					_type = "Type_" + str(z)					
					if (request.GET.get(_sets) != "" and request.GET.get(_reps) != ""):
						print(request.GET.get(_sets))
						print(request.GET.get(_reps))
						print(request.GET.get(_type))
						_Sets_ = request.GET.get(_sets)
						_Reps_ = request.GET.get(_reps)
						_Type_ = request.GET.get(_type)
						print("test")
						print(i[0] + " " + y[0] + " Subworkout " + str(z) + ": " 
						+ request.GET.get(_type) + " "
						+ str(request.GET.get(_sets)) + " x " + str(request.GET.get(_reps)))
						_SubWorkout = SubWorkout(Exercise_Type = _Type_, Sets = _Sets_, Reps = _Reps_, Order = z)
						_SubWorkout.save()
						if (_Workout_Template.SubWorkouts.all().filter(Order = z).exists()):
							print("Exists")							
							_Edit_SubWorkout = _Workout_Template.SubWorkouts.all().get(Order = z)

							_Edit_SubWorkout.Exercise_Type = _Type_
							_Edit_SubWorkout.Sets = _Sets_
							_Edit_SubWorkout.Reps = _Reps_
							_Edit_SubWorkout.save()
							_Workout_Template.save()
						else:
							_Workout_Template.SubWorkouts.add(_SubWorkout)
							_Workout_Template.save()
						# _Workout_Template.SubWorkouts.add(_SubWorkout)
						# _Workout_Template.save()
					# else:
					# 	print(i[0] + " " + y[0] + " No set ")
				return HttpResponseRedirect("/admin-site")

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

	if(request.GET.get("refresh")):
		return HttpResponseRedirect("/admin-site")

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

