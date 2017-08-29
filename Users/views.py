# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Workout, Set, Exercise, Member, SubWorkout, Workout_Template, Blog_Post
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, time, timedelta
from .forms import BlogPostForm
import json

Exercise_Types = ["UB Hor Push", "UB Vert Push",  "UB Hor Pull", "UB Vert Pull",  "Hinge", "Squat", "LB Uni Push", 
"Ant Chain", "Post Chain",  "Isolation", "Iso 2", "Iso 3", "Iso 4", "RFL Load", "RFD Unload 1", "RFD Unload 2"]

Levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

def User_Page(request): 
	workout_date_list = Workout.objects.values_list('_Date', flat=True).distinct()
	final_list = []

	for workout_date in workout_date_list:
		parsed_date_list = workout_date.split('/')
		parsed_date_dict = {}
		if (len(parsed_date_list) == 3): 
			parsed_date_dict[str('month')] = str(parsed_date_list[0])
			parsed_date_dict[str('day')] = str(parsed_date_list[1])
			parsed_date_dict[str('year')] = str(parsed_date_list[2])
			final_list.append(parsed_date_dict)

	return render(request, "userpage.html", {'final_list': json.dumps(final_list)})

Level_Names = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", "Level 8", "Level 9", "Level 10", "Level 11", "Level 12", "Level 13", "Level 14", "Level 15",
"Level 16", "Level 17", "Level 18", "Level 19", "Level 20", "Level 21", "Level 22", "Level 23", "Level 24", "Level 25"]

def Videos(request): 
	# _User = request.user
	# _Member = Member.objects.get(User = _User)
	# _Level = Member.Level
	context = {}
	context["Videos"] = []
	context["Levels"] = Levels

	context["Current_Level"] = []

	context["Display_Levels"] = Level_Names

	context["Video_Group_1"] = []
	context["Video_Group_2"] = []
	context["Video_Group_3"] = []
	context["Video_Group_4"] = []

	_Exercises = Exercise.objects.all()

	# if 'Current_Level' in request.session.keys():
	# 	context["Current_Level"] = [request.session["Current_Level"]]

	for i in _Exercises:
		if i.Level <= 5:
			context["Video_Group_1"].append(i.Name)
		elif i.Level <= 10:
			context["Video_Group_2"].append(i.Name)
		elif i.Level <= 15:
			context["Video_Group_3"].append(i.Name)
		elif i.Level <= 20:
			context["Video_Group_4"].append(i.Name)
		elif i.Level <= 25:
			context["Video_Group_5"].append(i.Name)

	if request.GET.get("search_submit"):
		_Search_Entry = request.GET.get("search")
		_Search_Terms = _Search_Entry.split()
		_Level_String = request.GET.get("Level")
		print(_Level_String)
		if (_Level_String != "All Levels"):
			_Level_Split = _Level_String.split()
			_Level = int(_Level_Split[1])
		request.session['Current_Level'] = _Level_String
		context["Current_Level"] = [_Level_String]
		Last_Levels = []
		context["Display_Levels"] = Level_Names		
		# context["Display_Levels"].remove(_Level_String)		
		# if _Level != 0:
			# for i in context["Display_Levels"]:
			# 	if i != _Level_String:
			# 		Last_Levels.append(i)
			# context["Display_Levels"] = []
			# context["Display_Levels"].append(_Level_String)
			# context["Display_Levels"] = context["Display_Levels"] + Last_Levels
		# print("Searching:")
		# print(_Search_Entry)
		# print(_Search_Terms)
		# print(_Level)
		if (_Level_String == "All Levels"):
			context["Display_Levels"] = ["All Levels"] + Level_Names
			print("All Levels Selected")
		if (_Level_String != "All Levels" and _Level != 0):
			_Level_Num = int(_Level)
			_Exercises = Exercise.objects.filter(Level = _Level_Num)
			context["Display_Levels"] = [_Level_String] + Level_Names

		# remove second instance of selected level
		selected_level = context["Display_Levels"][0]
		levels = context["Display_Levels"]
		levels_length = len(context["Display_Levels"]); 

		for i in range(1,levels_length): 
			if (levels[i] == selected_level): 
				context["Display_Levels"] = levels[:i] + levels[i+1:]

		if _Search_Entry == "":
			for i in _Exercises:
				_Name = i.Name
				context["Videos"].append(_Name)
			return render(request, "videos.html", context)
		else:
			for i in _Exercises:
				_Name = i.Name				
				for _Term in _Search_Terms:
					print(_Term)
					print(_Term.lower())
					print(_Term.capitalize())
					if _Term in _Name:
						context["Videos"].append(_Name)
					elif _Term.capitalize() in _Name:
						context["Videos"].append(_Name)
					elif _Term.lower() in _Name: 
						context["Videos"].append(_Name)
			return render(request, "videos.html", context)
	return render(request, "videos.html", context)

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
		# _Templates = Workout_Template.objects.filter(Level_Group = 1)

		# for i in _Templates:
		# 	print("Existing Workout Template: " + "Week " + str(i.Week) + " Day " 
		# 	+ str(i.Day) + " Ordered ID: " + str(i.Ordered_ID) + " Level Group: " + str(i.Level_Group))
		count = 0
		print("Program Start Date: " + Start_Date.strftime('%m/%d/%Y'))		
		print("Selected Workout Days: ")		
		_Days = []
		for x in Days:
			_Days.append(Days_Of_Week[x])
		print(_Days)

		for i in range(1, 29): #i will be from 1 to 28
			if (Start_Date + timedelta(days=i)).weekday() in Days:
				Workout_Date = Start_Date + timedelta(days=i)
				count += 1				
				string_date = Workout_Date.strftime('%m/%d/%Y')

				_Workout_Template = Workout_Template.objects.get(Level_Group=1, Ordered_ID=count)
				# print("Workout Template: " + "Week " + str(_Workout_Template.Week) + " Day " 
				# + str(_Workout_Template.Day) + " Ordered ID: " + str(_Workout_Template.Ordered_ID) + " Level Group: " + str(_Workout_Template.Level_Group))				

				_Workout = Workout(Template=_Workout_Template, _Date=string_date, Level = Level)
				_Workout.save()

				for x in _Workout.Template.SubWorkouts.all():
					_Type = x.Exercise_Type
					x.Exercise = Exercise.objects.get(Type = _Type, Level = Level)
					x.save()
					_Workout.SubWorkouts.add(x)
					_Workout.save()
				print("Level " + str(_Workout.Level) + " Workout Created For: " + _Workout._Date + " (Week " + str(_Workout.Template.Week) + " Day " + str(_Workout.Template.Day) + ")")
				# print("Sets and Reps: ")
				for z in _Workout.SubWorkouts.all():
					print(z.Exercise.Name + " " + str(z.Sets) + " x " + str(z.Reps))
				# print(string_date)
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
	context["Days_Of_Week"] = [["Monday", 0],["Tuesday", 1], ["Wednesday", 2], ["Thursday", 3], ["Friday", 4], ["Saturday", 5], ["Sunday", 6]]
	if request.GET.get("Create_Workout"):
		_Level = int(request.GET.get("Level"))
		_Year = request.GET.get("Year")
		_Month = request.GET.get("Month")
		_Day = request.GET.get("Day")

		Day_1 = int(request.GET.get("Day_1"))
		Day_2 = int(request.GET.get("Day_2"))
		Day_3 = int(request.GET.get("Day_3"))

		print(Day_1)
		print(Day_2)
		print(Day_3)

		Year = int(_Year)
		if _Month[0] == '0':
			Month = int(_Month[1])
		else:
			Month = int(_Month)
		if _Day[0] == '0':
			Day = int(_Day[1])
		else:
			Day = int(_Day)

		_Workout_Templates = Workout_Template.objects.filter(Level_Group = 1)

		for i in _Workout_Templates:
			print("Existing Workout Template: " + "Week " + str(i.Week) + " Day " 
			+ str(i.Day) + " Ordered ID: " + str(i.Ordered_ID) + " Level Group: " + str(i.Level_Group))

		print(_Level)
		print(Year)
		print(Month)
		print(Day)

		print(Generate_Workouts(datetime(Year, Month, Day), _Level, [Day_1, Day_2, Day_3]))
		return HttpResponseRedirect('/test/')
	return render(request, "test.html", context)


@csrf_exempt 
def Workout_Update(request): 
	if request.method == 'POST': 
		if 'TempDate' in request.POST: 

			# test_var = date 
			test_var = request.POST['TempDate']

			workoutDict = {}

			# need to filter on user id here
			workout_list = Workout.objects.filter(_Date=test_var); 

			# If workout exists
			if (workout_list.exists()): 
				counter = 0 
				for workout in workout_list: 
					counter +=1 
					subworkout_list = workout.SubWorkouts.all()
					subworkout_counter = 0 
					 
					for subworkout in subworkout_list: 
						subworkoutDict = {
							'level': str(workout.Level), # for now, extract levels for each subworkout
							'exercise_type': subworkout.Exercise_Type,
							'exercise_name': subworkout.Exercise.Name,
							'sets': str(subworkout.Sets),
							'reps': str(subworkout.Reps),
							'rpe': str(subworkout.RPE),
							'date': workout._Date
						}
						workoutDict[subworkout_counter] = subworkoutDict
						subworkout_counter += 1
			else: 
				subworkout_num = 6
				subworkoutDict = {
					'level': '',
					'exercise_type': '',
					'exercise_name': '',
					'sets': '',
					'reps': '',
					'rpe': '',
					'date': ''
				}
				for i in range(subworkout_num): 
					workoutDict[i] = subworkoutDict
		
			return JsonResponse(workoutDict)
		else: 
			return JsonResponse({'status': 'fail'})	


@csrf_exempt 
def RPE_Update(request): 
	if request.method == 'POST': 
		current_date = request.POST['current_date']
		# need to filter on user id here
		workout_list = Workout.objects.filter(_Date=current_date);

		for workout in workout_list: 
				subworkout_list = workout.SubWorkouts.all()
				subworkout_counter = 0 
				 
				for subworkout in subworkout_list: 
					if (subworkout_counter == 0): 
						subworkout.RPE = request.POST['RPE_row1']
						subworkout.save()
						workout.save()
					elif (subworkout_counter == 1): 
						subworkout.RPE = request.POST['RPE_row2']
						subworkout.save()
						workout.save()
					elif (subworkout_counter == 2): 
						subworkout.RPE = request.POST['RPE_row3']
						subworkout.save()
						workout.save()
					elif (subworkout_counter == 3): 
						subworkout.RPE = request.POST['RPE_row4']
						subworkout.save()
						workout.save()
					elif (subworkout_counter == 4): 
						subworkout.RPE = request.POST['RPE_row5']
						subworkout.save()
						workout.save()
					
					# subworkoutDict = {
					# 	'level': str(workout.Level),
					# 	'exercise_type': subworkout.Exercise_Type,
					# 	'exercise_name': subworkout.Exercise.Name,
					# 	'sets': str(subworkout.Sets),
					# 	'reps': str(subworkout.Reps),
					# 	'date': workout._Date
					# }
					# workoutDict[subworkout_counter] = subworkoutDict
					subworkout_counter += 1

		return HttpResponse('success'); 


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
	["Week 1", [["Day 1", [[], [], [], [], [], []], "D1"], ["Day 2", [[], [], [], [], [], []], "D2"], ["Day 3", [[], [], [], [], [], []], "D3"]], "W1"], 
	["Week 2", [["Day 1", [[], [], [], [], [], []], "D1"], ["Day 2", [[], [], [], [], [], []], "D2"], ["Day 3", [[], [], [], [], [], []], "D3"]], "W2"], 
	["Week 3", [["Day 1", [[], [], [], [], [], []], "D1"], ["Day 2", [[], [], [], [], [], []], "D2"], ["Day 3", [[], [], [], [], [], []], "D3"]], "W3"], 
	["Week 4", [["Day 1", [[], [], [], [], [], []], "D1"], ["Day 2", [[], [], [], [], [], []], "D2"], ["Day 3", [[], [], [], [], [], []], "D3"]], "W4"]]

	for i in Workout_Template.objects.all():
		_week_index = i.Week - 1 #Workout_Templates[index]
		_day_index = i.Day - 1 #Workout_Templates[week][1][_day_index]		

		# i.Level_Group = 1
		# i.save()
		print("Existing Workout Template: " + "Week " + str(i.Week) + " Day " + str(i.Day) + " Ordered ID: " + str(i.Ordered_ID) + " Level Group: " + str(i.Level_Group))

		Num_Sets = i.SubWorkouts.all().count()
		Empty_Sets = 6 - i.SubWorkouts.all().count()

		for x in i.SubWorkouts.all():			
			_exercise_type = x.Exercise_Type
			_sets = x.Sets
			_reps = x.Reps			
			_order = x.Order
			print(x.Exercise_Type + " " + str(x.Sets) + " x " + str(x.Reps)) + " (Set " + str(x.Order) + ")"
			_subworkout_index = x.Order - 1
			_rpe = ""
			_deload = ""
			_money = ""
			if x.RPE != 0:
				_rpe = x.RPE
			if x.Deload != 0:
				_deload = x.Deload
			if x.Money != 0:
				_money = str(x.Money) + "+" 
			context["Workout_Templates"][_week_index][1][_day_index][1][_subworkout_index] = [_exercise_type, str(_sets) + " x ", 
			_reps, "Set " + str(_order) + ":", _sets, _order, _rpe, _deload, _money]

		for y in range(1, Empty_Sets + 1):
			Empty_Index = Num_Sets - 1 + y
			context["Workout_Templates"][_week_index][1][_day_index][1][Empty_Index] = ["", "", "", "Set " + str(Empty_Index + 1) + ":", "", Empty_Index + 1, "", "", ""]



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
					# if (_Workout_Template.SubWorkouts.all().filter(Order = z).exists()):
					# 	_Placeholder_SubWorkout = _Workout_Template.SubWorkouts.all().get(Order = z)
						
					# 	_Type = _Placeholder_SubWorkout.Exercise_Type
					# 	_Sets = _Placeholder_SubWorkout.Sets
					# 	_Reps = _Placeholder_SubWorkout.Reps
						# context["Placeholders"][_week - 1][_day - 1][z - 1] = [_Type, _Sets, _Reps]
					_sets = "Sets_" + str(z)
					_reps = "Reps_" + str(z)
					_type = "Type_" + str(z)					
					_rpe = "RPE_" + str(z)
					_deload = "Deload_" + str(z)
					_money = "Money_" + str(z)
					if (request.GET.get(_type) != "" and (request.GET.get(_sets) != "" or request.GET.get(_reps) != ""
						or request.GET.get(_rpe) != "" or request.GET.get(_deload) != "" or request.GET.get(_money) != "")):
						print(request.GET.get(_sets))
						print(request.GET.get(_reps))
						print(request.GET.get(_type))
						print(request.GET.get(_rpe))
						print(request.GET.get(_money))
						_Sets_ = request.GET.get(_sets)
						_Reps_ = request.GET.get(_reps)
						_Type_ = request.GET.get(_type)
						_RPE = request.GET.get(_rpe)
						_Deload = request.GET.get(_deload)
						_Money = request.GET.get(_money)
						print("test")
						print(i[0] + " " + y[0] + " Subworkout " + str(z) + ": " 
						+ request.GET.get(_type) + " "
						+ str(request.GET.get(_sets)) + " x " + str(request.GET.get(_reps)))
						_SubWorkout = SubWorkout(Exercise_Type = _Type_, Order = z)
						if _Sets_ != "":
							_SubWorkout.Sets = _Sets_
						if _Reps_ != "":
							_SubWorkout.Reps = _Reps_
						if _RPE != "":
							_SubWorkout.RPE = _RPE
						if _Deload != "":
							_SubWorkout.Deload = _Deload 
						if _Money != "":
							_SubWorkout.Money = _Money
						_SubWorkout.save()
						if (_Workout_Template.SubWorkouts.all().filter(Order = z).exists()):
							print("Exists")							
							_Edit_SubWorkout = _Workout_Template.SubWorkouts.all().get(Order = z)

							_Edit_SubWorkout.Exercise_Type = _Type_
							if _Sets_ != "":
								_Edit_SubWorkout.Sets = _Sets_
							if _Reps_ != "":
								_Edit_SubWorkout.Reps = _Reps_
							if (_RPE != ""):
								_Edit_SubWorkout.RPE = _RPE
							if _Deload != "":
								_Edit_SubWorkout.Deload = _Deload 								
							if _Money != "":
								_Edit_SubWorkout.Money = _Money
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

Level_Group_1_Exercises = [["UB Hor Push", "UB Vert Push",  "UB Hor Pull", "UB Vert Pull",  "Hinge", "Squat"], 
["LB Uni Push", "Ant Chain", "Post Chain",  "Isolation", "Iso 2", "Iso 3", "Iso 4"]]

def AdminExercises(request):
	context = {}

	LG_1_Exercises = [
	[["UB Hor Push", ["", "", "", "", ""], "HPush"], ["UB Vert Push", ["", "", "", "", ""], "VPush"],  
	["UB Hor Pull", ["", "", "", "", ""], "HPull"], ["UB Vert Pull", ["", "", "", "", ""], "VPull"], 
	["Hinge", ["", "", "", "", ""], "H"], ["Squat", ["", "", "", "", ""], "S"]],

	[["LB Uni Push", ["", "", "", "", ""], "UniPush"], ["Ant Chain", ["", "", "", "", ""], "AC"], 
	["Post Chain", ["", "", "", "", ""], "PC"], ["Isolation", ["", "", "", "", ""], "I1"], 
	["Iso 2", ["", "", "", "", ""], "I2"], ["Iso 3", ["", "", "", "", ""], "I3"], 
	["Iso 4", ["", "", "", "", ""], "I4"]]]


	for Group in LG_1_Exercises:
		for x in Group:
		# for x in LG_1_Exercises[0]:
			_Type = x[0]
			for n in range(1, 6):
				# Input_Code = "L" + str(n) + x[2]
				# print(Input_Code)
				if Exercise.objects.filter(Type = _Type, Level = n).exists():
					_Exercise = Exercise.objects.get(Type = _Type, Level = n)
					x[1][n - 1] = _Exercise.Name
					print(_Exercise.Name)
				else:
					x[1][n - 1] = "Level " + str(n) + " Exercise"

	if request.GET.get("Update_Exercises"):
		for Group in LG_1_Exercises:
			for x in Group:
		# for x in LG_1_Exercises[0]:
				_Type = x[0]
				_ID = x[2]
				print(_ID)
				for n in range(1, 6):
					Input_Code = "L" + str(n) + x[2]
					# print(Input_Code)
					if request.GET.get(Input_Code) != "":
						_Name = request.GET.get(Input_Code)
						print(Input_Code + " : " + _Name)
						if Exercise.objects.filter(Type = x[0], Level = n).exists():
							_Exercise = Exercise.objects.get(Type = _Type, Level = n)
							_Exercise.Name = _Name
							_Exercise.Code = Input_Code
							_Exercise.save()
						else:
							_Exercise = Exercise(Type = x[0], Level = n, Name = _Name, Code = Input_Code)
							_Exercise.save()
		return HttpResponseRedirect("/admin-exercises")

	context["Exercises_1"] = LG_1_Exercises[0]
	context["Exercises_2"] = LG_1_Exercises[1]

	context["Levels"] = [[1, []],[2, []],[3, []],[4, []],[5, []]]

	Exercises_List_1 = []

	for i in Exercise.objects.all():
		row = []
		row.append(i.Type)
		row.append(i.Level)
		row.append(i.Name)
		row.append(i.Bodyweight)
		print(row)
		Exercises_List_1.append(row)


	return render(request, "adminexercises.html", context)

def Blog(request): 

	form = BlogPostForm()
	return render(request, 'blog.html', {'form': form})

	# FOR CLIENT SIDE (later)

	# blog_posts = Blog_Post.objects.order_by('-created_date')

	# return render(request, "blog.html", {'blog_posts': blog_posts }); 




