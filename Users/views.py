# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import stripe
from .models import Workout, Set, Exercise, Member, SubWorkout, Workout_Template, Video
from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, time, timedelta
import json
from django.contrib.auth import logout, login, authenticate
from django.core.files import File

Exercise_Types = ["UB Hor Push", "Hinge", "Squat", "UB Vert Push",  "UB Hor Pull", "UB Vert Pull",  "LB Uni Push", 
"Ant Chain", "Post Chain",  "Isolation", "Iso 2", "Iso 3", "Iso 4", "RFL Load", "RFD Unload 1", "RFD Unload 2"]

Levels = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]

def User_Page(request): 
	user = request.user
	print(user.username)
	_Member = Member.objects.get(User=user)
	Member_Workouts = Workout.objects.filter(Member = _Member)
	workout_date_list = Member_Workouts.values_list('_Date', flat=True).distinct()
	_First_Name = user.first_name 
	_Last_Name = user.last_name
	# workout_date_list = Workout.objects.values_list('_Date', flat=True).distinct()
	final_list = []

	for workout_date in workout_date_list:
		parsed_date_list = workout_date.split('/')
		parsed_date_dict = {}
		if (len(parsed_date_list) == 3): 
			parsed_date_dict[str('month')] = str(parsed_date_list[0])
			parsed_date_dict[str('day')] = str(parsed_date_list[1])
			parsed_date_dict[str('year')] = str(parsed_date_list[2])
			final_list.append(parsed_date_dict)

	return render(request, "userpage.html", {'first_name': _First_Name, 'final_list': json.dumps(final_list)})

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
	_Videos = Video.objects.all()

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
		if request.GET.get(str(i.pk)):
			print("PK Submitted: " + str(i.pk) + " " + i.Name)

	context["Video_URL"] = ""

	for i in _Videos:
		if request.GET.get(str(i.pk)):
			print("Video PK Submitted: " + str(i.pk) + " " + i.Title)
			request.session["Video_PK"] = i.pk
			context["Video_URL"] = "/" + i.File.url
			context["Video_Title"] = i.Title
			return render(request, "videos.html", context)



	if request.method == "GET":
		print("Form Submitted")
		print("Video PK: " + str(request.GET.get("Video_PK")))
	if request.method == "POST":
		print("POST DETECTED")
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

		if _Search_Entry == "":
			for i in _Videos:
				row = []
				_Name = i.Title
				row.append(_Name)
				row.append(i.pk)
				context["Videos"].append(row)
			# for i in _Exercises:
			# 	_Name = i.Name
			# 	row = []
			# 	row.append(_Name)
			# 	row.append(i.pk)
			# 	context["Videos"].append(row)
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
# def Test(request):
# 	return render(request, "")


Days_Of_Week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def Generate_Workouts(Start_Date, Level, Days_List, _Username):
	Week_Days = enumerate(Days_Of_Week)
	Days = Days_List
	# Workouts = Workout_Template.objects.get(Level=Level)
	_User = User.objects.get(username= _Username)
	_Member = Member.objects.get(User = _User)

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
				_Workout.Member = _Member 
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

def Create_User(email, first_name, last_name, squat, bench, bodyweight, Stripe_ID, RPE_Bool, Start_Date, Workout_Days):
	New_User = User.objects.create(username=email, first_name=first_name,last=last_name)
	New_User.save()
	New_Member = Member(User=New_User, Stripe_ID=Stripe_ID, SignUp_Day=datetime.now())
	New_Member.save()
	if squat <= bodyweight:
		New_Member.Level = 1
	elif squat > 1.5*bodyweight and bench > bodyweight and RPE_Bool:
		New_Member.Level = 11
	else:
		New_Member.Level = 6
	New_Member.save()
	Generate_Workouts(Start_Date, New_Member.Level, Workout_Days, email)
	# Generate Workouts Here



def Stripe_Test(request):
	context={}
	context["Usernames"] = []
	context["Payment_Status"] = ""
	
	for i in User.objects.all():
		context["Usernames"].append(i.username)
		if Member.objects.filter(User = i).exists() == False:
			_Member = Member(User = i)
			_Member.save()

	stripe.api_key = "sk_test_LKsnEFYm74fwmLbyfR3qKWgb"

	print(stripe.Subscription.list())

	for i in stripe.Customer.all():
		print("Stripe Customer: " + i.email)

	_Matt_User = User.objects.get(username = "matthewchan2147@gmail.com")
	_Matt_Member = Member.objects.get(User = _Matt_User)
	_Matt_Stripe_ID = _Matt_Member.Stripe_ID
	print(_Matt_Stripe_ID)
	_Matt_Customer = stripe.Customer.retrieve(_Matt_Member.Stripe_ID)
	print("Found Customer: " + _Matt_Customer.email)

	if request.GET.get("Subscribe_Input"):
		print("Subscribe: " + request.GET.get("Subscribe_Username"))
		_Username = request.GET.get("Subscribe_Username")
		_User = User.objects.get(username = _Username)
		_Member = Member.objects.get(User = _User)
		_ID = _Member.Stripe_ID
		_Customer = stripe.Customer.retrieve(_ID)
		print("Subscribe customer: " + _Customer.email)

		stripe.Subscription.create(
		  customer=_ID,
		  items=[
		    {
		      "plan": "1",
		    },
		  ]
		)

	Charge_Amount = 10000000

	if request.method == "POST":
		print("Post detected")
		Number = request.POST.get("cardnumber")
		print(Number)
		token = request.POST.get('stripeToken') # Using Flask
		_Username = request.POST.get("Username")
		_User = User.objects.get(username = _Username)
		_Member = Member.objects.get(User = _User)

		if (_Member.Stripe_Created == False):
			# charge = stripe.Charge.create(
			#   amount=Charge_Amount,
			#   currency="usd",
			#   customer=customer.id,
			# )
			try:
				customer = stripe.Customer.create(
					 	email=_Username,
					  	source=token,
					)
				_ID = customer.id
				charge = stripe.Charge.create(
			          amount=Charge_Amount, # new_order.total * 100
			          currency="usd",
			          customer=_ID,
			          # source=token,
			          description="Example charge"
			    )
				# _Member.Stripe_Created = True
				# _Member.Stripe_ID = customer.id
				# _Member.save()
				# print("New Customer Charged! Amount: " + str(charge.amount))
				# print("Username: " + _Username)
				# break
				return HttpResponseRedirect("/userpage")
			except stripe.error.CardError:
			    	print("Card Error - PAYMENT DECLINED")
			    	context["Payment_Status"] = "Payment Failed!"
				return render(request, "stripe_test.html", context)
		      	# The card has been declined
		      	# pass
		else:
			_ID = _Member.Stripe_ID
			_Customer = stripe.Customer.retrieve(_ID)
			charge = stripe.Charge.create(
			  amount=Charge_Amount,
			  currency="usd",
			  customer=_ID,
			)
			print("Existing Customer Charged: " + _Customer.email + " Amount: " + str(charge.amount))
			print("Charge Outcome: " + str(charge.outcome))
			return HttpResponseRedirect("/userpage")

		# customer = stripe.Customer.create(
		#   email="paying.user@example.com",
		#   source=token,
		# )


	if request.POST.get("Post_Test"):
		print("Post Test")

	if request.POST.get("payment_submit"):
		print("Payment Submitted")

	if request.POST.get("payment-form"):
		print("Payment Submitted (Input)")

	return render(request, "stripe_test.html", context)

def Test(request):
	context = {}
	context["Days_Of_Week"] = [["Monday", 0],["Tuesday", 1], ["Wednesday", 2], ["Thursday", 3], ["Friday", 4], ["Saturday", 5], ["Sunday", 6]]
	context["Usernames"] = []
	context["Workout_Display"] = []

	_User = request.user
	print(_User)
	print(_User.username)

	if request.GET.get("Login"):
		_Username = request.GET.get("Username")
		_Password = request.GET.get("Password")
		user = authenticate(username=_Username, password=_Password)
		if user is not None:
	    	    login(request, user)
		return HttpResponseRedirect('/test/')

	if request.GET.get("Logout"):
		logout(request)
		return HttpResponseRedirect('/test/')

	for i in User.objects.all():
		context["Usernames"].append(i.username)

	if request.GET.get("Show_Workouts"):
		_Username = request.GET.get("Username")
		print(_Username)
		_User = User.objects.get(username=_Username)
		_Member = Member.objects.get(User = _User)
		print("From Member: " + _Member.User.username)
		_Workouts = Workout.objects.filter(Member = _Member)
		for i in _Workouts:
			row = []
			_Week = i.Template.Week
			_Day = i.Template.Day
			print("Workout: " + "Level " + str(i.Level) + " Workout: " + " (Week " + str(i.Template.Week) + " Day " + str(i.Template.Day) + ", " + i._Date)
			row.append("Level " + str(i.Level) + " Workout: " + " (Week " + str(_Week) + " Day " + str(_Day) + ", " + i._Date + ")")
			row.append([])
			for x in i.SubWorkouts.all():
				row[1].append(x.Exercise.Name + " " + str(x.Sets) + " " + str(x.Reps))
				print(x.Exercise.Name + " " + str(x.Sets) + " " + str(x.Reps))
			context["Workout_Display"].append(row)
		return render(request, "test.html", context)

	if request.GET.get("Create_Workout"):
		_Level = int(request.GET.get("Level"))
		_Year = request.GET.get("Year")
		_Month = request.GET.get("Month")
		_Day = request.GET.get("Day")

		_Username = request.GET.get("Username")
		print("Username for workouts: " + _Username)

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

		print(Generate_Workouts(datetime(Year, Month, Day), _Level, [Day_1, Day_2, Day_3], _Username))
		return HttpResponseRedirect('/test/')
	if request.GET.get("Create_User"):
		print("Create User")
		Username = request.GET.get("Username")
		PWord_1 = request.GET.get("Password_1")
		PWord_2 = request.GET.get("Password_2")
		First_Name = request.GET.get("F_Name")
		Last_Name = request.GET.get("L_Name")
		if (Username != "" and PWord_1 != "" and PWord_2 != "" and PWord_1 == PWord_2):
			print("Username: " + Username)
			print("Password 1: " + PWord_1)
			print("Password 2: " + PWord_2)
			print("First Name: " + First_Name)
			print("Last Name: " + Last_Name)
			_User = User.objects.create(username=Username, first_name=First_Name, last_name=Last_Name, password = PWord_1)
			_User.set_password(PWord_2)
			_User.save()
			_User.is_active = True
			_User.save()
			_Member = Member(User=_User)
			_Member.save()

		# CREATE STRIPE CUSTOMER HERE TOO
			# if request.method == "POST":
			# 	token = request.POST.get('stripeToken') 
				# if (_Member.Stripe_Created == False):
				# 	customer = stripe.Customer.create(
				# 	 	email=Username,
				# 	  	source=token,
				# 	)
				# 	charge = stripe.Charge.create(
				# 	  amount=1000,
				# 	  currency="usd",
				# 	  customer=customer.id,
				# 	)
				# _Member.Stripe_ID = _customer.id
				# _Customer = stripe.Customer.retrieve(_Member.Stripe_ID)
				# if request.GET.get("Subscribe_Input"):
				# 	print("Subscribe: " + request.GET.get("Subscribe_Username"))
				# 	_ID = _Member.Stripe_ID
				# 	_Customer = stripe.Customer.retrieve(_ID)
				# 	print("Subscribe customer: " + _Customer.email)
				# 	stripe.Subscription.create(
				# 	  customer=_ID,
				# 	  items=[
				# 	    {
				# 	      "plan": "1",
				# 	    },
				# 	  ]
				# 	)				
				# 	_Member.Stripe_Created = True;
				# 	_Member.Stripe_ID = customer.id;
				# 	_Member.save()
				# 	print("New Customer Charged! Amount: " + str(charge.amount))
				# 	print("Username: " + _Username)
				# else:
				# 	_ID = _Member.Stripe_ID
				# 	_Customer = stripe.Customer.retrieve(_ID)
				# 	charge = stripe.Charge.create(
				# 	  amount=1000,
				# 	  currency="usd",
				# 	  customer=_ID,
				# 	)
				# 	print("Existing Customer Charged: " + _Customer.email + " Amount: " + str(charge.amount))

		context["User_Added"] = "User Added"
		return HttpResponseRedirect('/test/')
	return render(request, "test.html", context)

@csrf_exempt 
def Workout_Update(request): 
	_User = request.user
	_Member = Member.objects.get(User=_User)
	if request.method == 'POST': 
		if 'TempDate' in request.POST: 

			# test_var = date 
			test_var = request.POST['TempDate']
			print "Request is", request 
			print test_var
			print isinstance(test_var, basestring)

			workoutDict = {}

			# need to filter on user id here
			if Workout.objects.filter(_Date=test_var, Member=_Member).exists() == False:
				_Empty_Dict = {
						'level': '', # for now, extract levels for each subworkout
						'exercise_type': '',
						'exercise_name': '',
						'sets': '',
						'reps': '',
						'rpe': '',
						'date': ''
					}
				workoutDict[0] = _Empty_Dict
				workoutDict[1] = _Empty_Dict
				workoutDict[2] = _Empty_Dict
				workoutDict[3] = _Empty_Dict
				workoutDict[4] = _Empty_Dict
				workoutDict[5] = _Empty_Dict
				return JsonResponse(workoutDict)
			workout_list = Workout.objects.filter(_Date=test_var, Member=_Member) 
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
			print workoutDict	
			return JsonResponse(workoutDict)
		else: 
			return JsonResponse({'status': 'fail'})	 

@csrf_exempt 
def RPE_Update(request): 
	_User = request.user
	_Member = Member.objects.get(User=_User)

	if request.method == 'POST': 
		current_date = request.POST['current_date']
		# need to filter on user id here
		workout_list = Workout.objects.filter(_Date=current_date, Member=_Member);

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

def Admin_Workouts(request):
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

	for i in Workout_Template.objects.filter(Level_Group=1):
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
				return HttpResponseRedirect("/admin-workouts")

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
		return HttpResponseRedirect("/admin-workouts")

	if(request.GET.get("delete_all")):
		Member.objects.all().delete()
		Exercise.objects.all().delete()
		Set.objects.all().delete()
		Workout.objects.all().delete()
		SubWorkout.objects.all().delete()
		return HttpResponseRedirect("/admin-workouts")

	if(request.GET.get("delete_sets_workouts")):
		Set.objects.all().delete()
		Workout.objects.all().delete()
		return HttpResponseRedirect("/admin-workouts")

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
		return HttpResponseRedirect("/admin-workouts")
	#ADDING EXERCISES 
	if(request.GET.get("submitaddexercise")):
		context["Exercise_Added"] = "Exercise Added"

		exercise_name = request.GET.get("exercise_name")
		exercise_type = request.GET.get("exercise_type")
		exercise_level = request.GET.get("exercise_level")

		if Exercise.objects.filter(Name=exercise_name).exists() == False:
			new_exercise = Exercise(Name=exercise_name, Type=exercise_type, Level=exercise_level)
			new_exercise.save()
		return HttpResponseRedirect("/admin-workouts")

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
		return HttpResponseRedirect("/admin-workouts")

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
		return HttpResponseRedirect("/admin-workouts")
		# return render(request, "admin.html", context)	
	return render(request, "admin_workouts.html", context)

def Admin_Workouts_2(request):
	context = {}
	context["Users"] = []

	context["Exercise_Types"] = Exercise_Types
	SubWorkouts = [[1], [2], [3], [4], [5], [6], [7]]
	context["Workout_Templates"] = [
	["Week 1", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W1", 1], 
	["Week 2", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W2", 2], 
	["Week 3", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W3", 3], 
	["Week 4", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3]], "W4", 4]]

	_Templates = Workout_Template.objects.filter(Level_Group=2)
	for i in _Templates:
		print("Level Group 2 Template: " + str(i.Week) + " " + str(i.Day))
		for x in i.SubWorkouts.all():
			print(x.Exercise_Type)
		# i.delete()

	N_SubWorkouts = len(SubWorkouts)

	for i in context["Workout_Templates"]:
		_Max_Index = len(i)
		_Week = i[_Max_Index - 1]
		_Week_Code = i[_Max_Index - 2]
		for _D in i[1]:
			# print(i[0] + " " + _D[0])
			_D[1] = [[1], [2], [3], [4], [5], [6], [7]]
			_Day = _D[3]
			_Day_Code = _D[2]
			_Btn_Code = _Week_Code + _Day_Code + "_Update_Workout"
			if Workout_Template.objects.filter(Level_Group=2, Week=_Week, Day=_Day).exists() == False:
				_Template = Workout_Template(Level_Group=2, Week=_Week, Day=_Day)
				_Template.Ordered_ID = (_Week - 1)*4 + _Day
				_Template.save()
				# print("Created Workout Template: W" + str(_Week) + " D" + str(_Day) + " Ordered ID: " + str(_Template.Ordered_ID))
			else:
				_Template = Workout_Template.objects.get(Level_Group=2, Week=_Week, Day=_Day)
				_Template.Ordered_ID = (_Week - 1)*4 + _Day
				_Template.save()
				# print("Existing Workout Template: W" + str(_Template.Week) + " D" + str(_Template.Day) + " Ordered ID: " + str(_Template.Ordered_ID))
			_Template_Code = _Week_Code + _Day_Code + " " + str(_Template.Ordered_ID)
			# print(_D[1])
			# DISPLAY HANDLED HERE
			print(_Template_Code)
			for _S in _D[1]:
				_Index = _D[1].index(_S)
				_Sub_Index = _Index + 1
				# _S.append(_Index + 1)
				# _S = [_Index + 1]
				# print(_Index)
				# _S[0] = (_Index + 1)
				print(_S)
				_Template = Workout_Template.objects.get(Level_Group=2, Week=_Week, Day=_Day)
				if (_Template.SubWorkouts.all().filter(Order = _Sub_Index).exists()):
					_Sub = _Template.SubWorkouts.all().get(Order = _Sub_Index)
					# _S = [_Sub.Exercise_Type, _Sub.Sets, _Sub.RPE, _Sub.Deload, _Sub.Money]
					_S.append(_Sub.Exercise_Type)
					_S.append(_Sub.Sets)
					_S.append(_Sub.Reps)
					_S.append(_Sub.RPE)
					_S.append(_Sub.Deload)
					_S.append(_Sub.Money)
				else :
					_S = _S + ["", "", "", "", "", ""]
			for _S in _Template.SubWorkouts.all():
				print("Subworkout for: " + _Template_Code)

			if request.GET.get(_Btn_Code):
				print("Button Pressed for: " + _Template_Code)
				for i in range(1, N_SubWorkouts + 1):					
					# print(i)
					_Sub_Index = i
					_Sets = "Sets_" + str(i)
					_Reps = "Reps_" + str(i)
					_Type = "Type_" + str(i)
					_RPE = "RPE_" + str(i)
					_Deload = "Deload_" + str(i)
					_Alloy = "Alloy_" + str(i)
					Type = request.GET[_Type] 
					Sets = request.GET[_Sets] 
					Reps = request.GET[_Reps] 					
					if (Type != "" and Sets != "" and Reps != ""):
						print (_Template_Code + " Subworkout Changed: " + str(i))
						# print(request.GET[_Type])
						RPE = request.GET[_RPE]
						Deload = request.GET[_Deload]
						Alloy = request.GET[_Alloy]
						if (_Template.SubWorkouts.all().filter(Order = _Sub_Index).exists()):
							_Subworkout = _Template.SubWorkouts.all().get(Order = _Sub_Index)
							_Subworkout.Type = Type
							_Subworkout.Sets = Sets
							_Subworkout.Reps = Reps
							if RPE != "":
								_Subworkout.RPE = RPE
							if Deload != "":
								_Subworkout.Deload = Deload
							if Alloy != "":
								_Subworkout.Money = Alloy
							_Subworkout.save()					
							_Template.save()		
						else:
							_Subworkout = SubWorkout(Order=_Sub_Index, Exercise_Type=Type, Sets=Sets, Reps=Reps)
							_Subworkout.save()
							if RPE != "":
								_Subworkout.RPE = RPE
							if Deload != "":
								_Subworkout.Deload = Deload
							if Alloy != "":
								_Subworkout.Money = Alloy
							_Subworkout.save()
							_Template.SubWorkouts.add(_Subworkout)
							_Template.save()
				return HttpResponseRedirect("/admin-workouts-2")
	# print(context["Workout_Templates"])		
	return render(request, "admin_workouts_2.html", context)
def Admin_Workouts_3(request):
	context = {}
	context["Users"] = []

	context["Exercise_Types"] = Exercise_Types
	SubWorkouts = [[1], [2], [3], [4], [5], [6], [7]]

	context["Blocks"] = [["Block 1 - Volume", "Block_1", 1], ["Block 2 - Strength/Power", "Block_2", 2]]
	context["Selected_Block"] = [["Block 1 - Volume", "Block_1", 1]]	

	if "Selected_Block" in request.session.keys():
		_Selected_Block = context["Blocks"][request.session["Selected_Block"] - 1]
		context["Selected_Block"] = [_Selected_Block]
		context["Blocks"].remove(_Selected_Block)
	else:
		request.session["Selected_Block"] = 1
		_Selected_Block = context["Blocks"][request.session["Selected_Block"] - 1]
		context["Selected_Block"] = [_Selected_Block]
		context["Blocks"].remove(_Selected_Block)

	if request.method == 'POST':
		if request.POST['Block'] == "Block_1":
			request.session["Selected_Block"] = 1
		elif request.POST['Block'] == "Block_2":
			request.session["Selected_Block"] = 2
		return HttpResponseRedirect("/admin-workouts-3")

	context["Workout_Templates"] = []

	Templates = [
	[["Week 1", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W1", 1], 
	["Week 2", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W2", 2], 
	["Week 3", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W3", 3], 
	["Week 4", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W4", 4]],
	
	[["Week 1", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W1", 1], 
	["Week 2", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W2", 2], 
	["Week 3", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W3", 3], 
	["Week 4", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W4", 4],
	["Week 5", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3]], "W5", 5]]]

	context["Block_Label"] = context["Selected_Block"][0][0]
	# if request.session["Selected_Block"] == 1:
	# 	context["Block_Label"] = context["Blocks"][0][0]
	# elif request.session["Selected_Block"] == 2:
	# 	context["Block_Label"] = context["Blocks"][1][0]

	Selected_Block = request.session["Selected_Block"]
	if Selected_Block == 1:
		context["Workout_Templates"] = Templates[0]
	elif Selected_Block == 2:
		context["Workout_Templates"] = Templates[1]

	_Templates = Workout_Template.objects.filter(Level_Group=3, Block_Num=Selected_Block)

	for i in _Templates:
		print("Level Group 3 Template: " + str(i.Week) + " " + str(i.Day) + " Block #: " + str(i.Block_Num))
		for x in i.SubWorkouts.all():
			print("	" + x.Exercise_Type + " " + str(x.Sets) + " x " + str(x.Reps))
		# i.delete()
	N_SubWorkouts = len(SubWorkouts)
	# for _Templates in context["Workout_Templates"]:
	if (3 == 3):
		for i in context["Workout_Templates"]:
			_Max_Index = len(i)
			_Week = i[_Max_Index - 1]
			_Week_Code = i[_Max_Index - 2]
			for _D in i[1]:
				# print(i[0] + " " + _D[0])
				_D[1] = [[1], [2], [3], [4], [5], [6], [7]]
				_Day = _D[3]
				_Day_Code = _D[2]
				_Btn_Code = _Week_Code + _Day_Code + "_Update_Workout"
				if Workout_Template.objects.filter(Level_Group=3, Week=_Week, Day=_Day, Block_Num=Selected_Block).exists() == False:
					_Template = Workout_Template(Level_Group=3, Week=_Week, Day=_Day, Block_Num=Selected_Block)
					_Template.Ordered_ID = (_Week - 1)*4 + _Day
					_Template.save()
					# print("Created Workout Template: W" + str(_Week) + " D" + str(_Day) + " Ordered ID: " + str(_Template.Ordered_ID))
				else:
					_Template = Workout_Template.objects.get(Level_Group=3, Week=_Week, Day=_Day, Block_Num=Selected_Block)
					_Template.Ordered_ID = (_Week - 1)*4 + _Day
					_Template.save()
					# print("Existing Workout Template: W" + str(_Template.Week) + " D" + str(_Template.Day) + " Ordered ID: " + str(_Template.Ordered_ID))
				_Template_Code = _Week_Code + _Day_Code + " " + str(_Template.Ordered_ID)
				# print(_D[1])
				# DISPLAY HANDLED HERE
				print(_Template_Code)
				for _S in _D[1]:
					_Index = _D[1].index(_S)
					_Sub_Index = _Index + 1
					# _S.append(_Index + 1)
					# _S = [_Index + 1]
					# print(_Index)
					# _S[0] = (_Index + 1)
					print(_S)
					_Template = Workout_Template.objects.get(Level_Group=3, Week=_Week, Day=_Day, Block_Num=Selected_Block)
					if (_Template.SubWorkouts.all().filter(Order = _Sub_Index).exists()):
						_Sub = _Template.SubWorkouts.all().get(Order = _Sub_Index)
						# _S = [_Sub.Exercise_Type, _Sub.Sets, _Sub.RPE, _Sub.Deload, _Sub.Money]
						_S.append(_Sub.Exercise_Type)
						_S.append(_Sub.Sets)
						_S.append(_Sub.Reps)
						_S.append(_Sub.RPE)
						_S.append(_Sub.Deload)
						_S.append(_Sub.Money)
					else :
						_S = _S + ["", "", "", "", "", ""]
				for _S in _Template.SubWorkouts.all():
					print("Subworkout for: " + _Template_Code)

				if request.GET.get(_Btn_Code):
					print("Button Pressed for: " + _Template_Code)
					for i in range(1, N_SubWorkouts + 1):					
						# print(i)
						_Sub_Index = i
						_Sets = "Sets_" + str(i)
						_Reps = "Reps_" + str(i)
						_Type = "Type_" + str(i)
						_RPE = "RPE_" + str(i)
						_Deload = "Deload_" + str(i)
						_Alloy = "Alloy_" + str(i)
						Type = request.GET[_Type] 
						Sets = request.GET[_Sets] 
						Reps = request.GET[_Reps] 					
						if (Type != "" and Sets != "" and Reps != ""):
							print (_Template_Code + " Subworkout Changed: " + str(i))
							# print(request.GET[_Type])
							RPE = request.GET[_RPE]
							Deload = request.GET[_Deload]
							Alloy = request.GET[_Alloy]
							if (_Template.SubWorkouts.all().filter(Order = _Sub_Index).exists()):
								_Subworkout = _Template.SubWorkouts.all().get(Order = _Sub_Index)
								_Subworkout.Type = Type
								_Subworkout.Sets = Sets
								_Subworkout.Reps = Reps
								if RPE != "":
									_Subworkout.RPE = RPE
								if Deload != "":
									_Subworkout.Deload = Deload
								if Alloy != "":
									_Subworkout.Money = Alloy
								_Subworkout.save()					
								_Template.save()		
							else:
								_Subworkout = SubWorkout(Order=_Sub_Index, Exercise_Type=Type, Sets=Sets, Reps=Reps)
								_Subworkout.save()
								if RPE != "":
									_Subworkout.RPE = RPE
								if Deload != "":
									_Subworkout.Deload = Deload
								if Alloy != "":
									_Subworkout.Money = Alloy
								_Subworkout.save()
								_Template.SubWorkouts.add(_Subworkout)
								_Template.save()
					return HttpResponseRedirect("/admin-workouts-3")
	# print(context["Workout_Templates"])		
	return render(request, "admin_workouts_3.html", context)

def Admin_Workouts_4(request):
	context = {}
	context["Users"] = []
	context["Exercise_Types"] = Exercise_Types
	SubWorkouts = [[1], [2], [3], [4], [5], [6], [7]]

	context["Blocks"] = [["Block 1 - Volume", "Block_1", 1], ["Block 2 - Strength/Power", "Block_2", 2]]
	context["Selected_Block"] = [["Block 1 - Volume", "Block_1", 1]]	

	if "Selected_Block" in request.session.keys():
		_Selected_Block = context["Blocks"][request.session["Selected_Block"] - 1]
		context["Selected_Block"] = [_Selected_Block]
		context["Blocks"].remove(_Selected_Block)
	else:
		request.session["Selected_Block"] = 1
		_Selected_Block = context["Blocks"][request.session["Selected_Block"] - 1]
		context["Selected_Block"] = [_Selected_Block]
		context["Blocks"].remove(_Selected_Block)

	if request.method == 'POST':
		if request.POST['Block'] == "Block_1":
			request.session["Selected_Block"] = 1
		elif request.POST['Block'] == "Block_2":
			request.session["Selected_Block"] = 2
		return HttpResponseRedirect("/admin-workouts-4")

	context["Workout_Templates"] = []

	Templates = [
	[["Week 1", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W1", 1], 
	["Week 2", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W2", 2], 
	["Week 3", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W3", 3], 
	["Week 4", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3]], "W4", 4]],
	
	[["Week 1", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W1", 1], 
	["Week 2", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W2", 2], 
	["Week 3", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3], ["Day 4", SubWorkouts, "D4", 4]], "W3", 3], 
	["Week 4", [["Day 1", SubWorkouts, "D1", 1], ["Day 2", SubWorkouts, "D2", 2], ["Day 3", SubWorkouts, "D3", 3]], "W4", 4]]]

	context["Block_Label"] = context["Selected_Block"][0][0]
	# if request.session["Selected_Block"] == 1:
	# 	context["Block_Label"] = context["Blocks"][0][0]
	# elif request.session["Selected_Block"] == 2:
	# 	context["Block_Label"] = context["Blocks"][1][0]

	Selected_Block = request.session["Selected_Block"]
	if Selected_Block == 1:
		context["Workout_Templates"] = Templates[0]
	elif Selected_Block == 2:
		context["Workout_Templates"] = Templates[1]

	_Templates = Workout_Template.objects.filter(Level_Group=4, Block_Num=Selected_Block)

	for i in _Templates:
		print("Level Group 4 Template: " + str(i.Week) + " " + str(i.Day) + " Block #: " + str(i.Block_Num))
		for x in i.SubWorkouts.all():
			print("	" + x.Exercise_Type + " " + str(x.Sets) + " x " + str(x.Reps))
		# i.delete()
	N_SubWorkouts = len(SubWorkouts)
	# for _Templates in context["Workout_Templates"]:
	if (3 == 3):
		for i in context["Workout_Templates"]:
			_Max_Index = len(i)
			_Week = i[_Max_Index - 1]
			_Week_Code = i[_Max_Index - 2]
			for _D in i[1]:
				# print(i[0] + " " + _D[0])
				_D[1] = [[1], [2], [3], [4], [5], [6], [7]]
				_Day = _D[3]
				_Day_Code = _D[2]
				_Btn_Code = _Week_Code + _Day_Code + "_Update_Workout"
				if Workout_Template.objects.filter(Level_Group=4, Week=_Week, Day=_Day, Block_Num=Selected_Block).exists() == False:
					_Template = Workout_Template(Level_Group=4, Week=_Week, Day=_Day, Block_Num=Selected_Block)
					_Template.Ordered_ID = (_Week - 1)*4 + _Day
					_Template.save()
					# print("Created Workout Template: W" + str(_Week) + " D" + str(_Day) + " Ordered ID: " + str(_Template.Ordered_ID))
				else:
					_Template = Workout_Template.objects.get(Level_Group=4, Week=_Week, Day=_Day, Block_Num=Selected_Block)
					_Template.Ordered_ID = (_Week - 1)*4 + _Day
					_Template.save()
					# print("Existing Workout Template: W" + str(_Template.Week) + " D" + str(_Template.Day) + " Ordered ID: " + str(_Template.Ordered_ID))
				_Template_Code = _Week_Code + _Day_Code + " " + str(_Template.Ordered_ID)
				# print(_D[1])
				# DISPLAY HANDLED HERE
				print(_Template_Code)
				for _S in _D[1]:
					_Index = _D[1].index(_S)
					_Sub_Index = _Index + 1
					# _S.append(_Index + 1)
					# _S = [_Index + 1]
					# print(_Index)
					# _S[0] = (_Index + 1)
					print(_S)
					_Template = Workout_Template.objects.get(Level_Group=4, Week=_Week, Day=_Day, Block_Num=Selected_Block)
					if (_Template.SubWorkouts.all().filter(Order = _Sub_Index).exists()):
						_Sub = _Template.SubWorkouts.all().get(Order = _Sub_Index)
						# _S = [_Sub.Exercise_Type, _Sub.Sets, _Sub.RPE, _Sub.Deload, _Sub.Money]
						_S.append(_Sub.Exercise_Type)
						_S.append(_Sub.Sets)
						_S.append(_Sub.Reps)
						_S.append(_Sub.RPE)
						_S.append(_Sub.Deload)
						_S.append(_Sub.Money)
					else :
						_S = _S + ["", "", "", "", "", ""]
				for _S in _Template.SubWorkouts.all():
					print("Subworkout for: " + _Template_Code)

				if request.GET.get(_Btn_Code):
					print("Button Pressed for: " + _Template_Code)
					for i in range(1, N_SubWorkouts + 1):					
						# print(i)
						_Sub_Index = i
						_Sets = "Sets_" + str(i)
						_Reps = "Reps_" + str(i)
						_Type = "Type_" + str(i)
						_RPE = "RPE_" + str(i)
						_Deload = "Deload_" + str(i)
						_Alloy = "Alloy_" + str(i)
						Type = request.GET[_Type] 
						Sets = request.GET[_Sets] 
						Reps = request.GET[_Reps] 					
						if (Type != "" and Sets != "" and Reps != ""):
							print (_Template_Code + " Subworkout Changed: " + str(i))
							# print(request.GET[_Type])
							RPE = request.GET[_RPE]
							Deload = request.GET[_Deload]
							Alloy = request.GET[_Alloy]
							if (_Template.SubWorkouts.all().filter(Order = _Sub_Index).exists()):
								_Subworkout = _Template.SubWorkouts.all().get(Order = _Sub_Index)
								_Subworkout.Type = Type
								_Subworkout.Sets = Sets
								_Subworkout.Reps = Reps
								if RPE != "":
									_Subworkout.RPE = RPE
								if Deload != "":
									_Subworkout.Deload = Deload
								if Alloy != "":
									_Subworkout.Money = Alloy
								_Subworkout.save()					
								_Template.save()		
							else:
								_Subworkout = SubWorkout(Order=_Sub_Index, Exercise_Type=Type, Sets=Sets, Reps=Reps)
								_Subworkout.save()
								if RPE != "":
									_Subworkout.RPE = RPE
								if Deload != "":
									_Subworkout.Deload = Deload
								if Alloy != "":
									_Subworkout.Money = Alloy
								_Subworkout.save()
								_Template.SubWorkouts.add(_Subworkout)
								_Template.save()
					return HttpResponseRedirect("/admin-workouts-4")
	return render(request, "admin_workouts_4.html", context)

Level_Group_1_Exercises = [["UB Hor Push", "UB Vert Push",  "UB Hor Pull", "UB Vert Pull",  "Hinge", "Squat"], 
["LB Uni Push", "Ant Chain", "Post Chain",  "Isolation", "Iso 2", "Iso 3", "Iso 4"]]

def AdminExercises(request):
	context = {}

	LG_1_Exercises = [
	[["UB Hor Push", ["", "", "", "", ""], "HPush"],
	["Hinge", ["", "", "", "", ""], "H"], ["Squat", ["", "", "", "", ""], "S"], 
	["UB Vert Push", ["", "", "", "", ""], "VPush"],  
	["UB Hor Pull", ["", "", "", "", ""], "HPull"], 
	["UB Vert Pull", ["", "", "", "", ""], "VPull"]],

	[["LB Uni Push", ["", "", "", "", ""], "UniPush"], ["Ant Chain", ["", "", "", "", ""], "AC"], 
	["Post Chain", ["", "", "", "", ""], "PC"], ["Isolation", ["", "", "", "", ""], "I1"], 
	["Iso 2", ["", "", "", "", ""], "I2"], ["Iso 3", ["", "", "", "", ""], "I3"], 
	["Iso 4", ["", "", "", "", ""], "I4"]],

	[["Metabolic Cond", ["", "", "", "", ""], "MC"], ["Work Capacity", ["", "", "", "", ""], "WC"], 
	["RFD Load", ["", "", "", "", ""], "RL"], ["RFD Unload 1", ["", "", "", "", ""], "RU1"], 
	["RFD Unload 2", ["", "", "", "", ""], "RU2"], ["Medicine Ball", ["", "", "", "", ""], "MB"]]
	]

	Level_Groups = [
	[["Level 1", "L1", [], [], []], ["Level 2", "L2", [], [], []], ["Level 3", "L3", [], [], []], ["Level 4", "L4", [], [], []], ["Level 5", "L5", [], [], []]],
	[["Level 6", "L6", [], [], []], ["Level 7", "L7", [], [], []], ["Level 8", "L8", [], [], []], ["Level 9", "L9", [], [], []], ["Level 10", "L10", [], [], []]],
	[["Level 11", "L11", [], [], []], ["Level 12", "L12", [], [], []], ["Level 13", "L13", [], [], []], ["Level 14", "L14", [], [], []], ["Level 15", "L15", [], [], []]],
	[["Level 16", "L16", [], [], []], ["Level 17", "L17", [], [], []], ["Level 18", "L18", [], [], []], ["Level 19", "L19", [], [], []], ["Level 20", "L20", [], [], []]],
	[["Level 21", "L21", [], [], []], ["Level 22", "L22", [], [], []], ["Level 23", "L23", [], [], []], ["Level 24", "L24", [], [], []], ["Level 25", "L25", [], [], []]]]

	# for i in Level_Groups:
	# 		for x in i:
	# 			if Level_Groups.index(i) != 0:
	# 				x = x + [[], [], []]
	# 			print(x)
	# print(Level_Groups[1])
	context["Level_Groups"] = [["1-5", 1], ["6-10", 2], ["11-15", 3], ["16-20", 4], ["21-25", 5]]
	# print("Context Levels: " + str(context["Levels"][0]))


	if request.method == "POST":
		# print("Post Detected")
		# print(request.POST["level_group"])
		L_Group = int(request.POST["level_group"])
		request.session["Level_Group"] = L_Group

	if "Level_Group" not in request.session.keys():
		request.session["Level_Group"] = 1

	Selected_L_Group_Index = request.session["Level_Group"] - 1
	Level_Constant = Selected_L_Group_Index*5

	context["Selected_Group"] = [context["Level_Groups"][Selected_L_Group_Index]]
	context["Level_Groups"].remove(context["Selected_Group"][0])
	context["Levels"] = Level_Groups[Selected_L_Group_Index]


	for Group in LG_1_Exercises:
		for x in Group:
		# for x in LG_1_Exercises[0]:
			Group_Index = LG_1_Exercises.index(Group)
			_Type = x[0]
			_Code = x[2]
			for n in range(1, 6):
				Level_Group_Index = n - 1
				Level_Num = n + Level_Constant
				# Input_Code = "L" + str(n) + x[2]
				# print(Input_Code)
				if Exercise.objects.filter(Type = _Type, Level = Level_Num).exists():
					_Exercise = Exercise.objects.get(Type = _Type, Level = Level_Num)
					x[1][n - 1] = _Exercise.Name
					if Group_Index == 0:
						context["Levels"][Level_Group_Index][2].append([_Exercise.Name, _Code])
					elif Group_Index == 1:
						context["Levels"][Level_Group_Index][3].append([_Exercise.Name, _Code])
					elif Group_Index == 2:
						context["Levels"][Level_Group_Index][4].append([_Exercise.Name, _Code])
					# print(_Exercise.Name)
				else:
					x[1][n - 1] = "Level " + str(n) + " Exercise"
					if Group_Index == 0:
						context["Levels"][Level_Group_Index][2].append(["Level " + str(Level_Num) + " Exercise", _Code])
					elif Group_Index == 1:
						context["Levels"][Level_Group_Index][3].append(["Level " + str(Level_Num) + " Exercise", _Code])
					elif Group_Index == 2:
						context["Levels"][Level_Group_Index][4].append(["Level " + str(Level_Num) + " Exercise", _Code])
	if request.GET.get("Update_Exercises"):
		for Group in LG_1_Exercises:
			for x in Group:
		# for x in LG_1_Exercises[0]:
				_Type = x[0]
				_ID = x[2]
				# print(_ID)
				for n in range(1, 6):
					Level_Num = n + Level_Constant
					Input_Code = "L" + str(Level_Num) + x[2]
					# print(Input_Code)
					if request.GET.get(Input_Code) != "" and request.GET.get(Input_Code) != None:
						_Name = request.GET.get(Input_Code)
						print(Input_Code + " " + _Name)
						print(Input_Code + " : " + _Name)
						if Exercise.objects.filter(Type = x[0], Level = Level_Num).exists():
							_Exercise = Exercise.objects.get(Type = _Type, Level = n)
							_Exercise.Name = _Name
							_Exercise.Code = Input_Code
							_Exercise.save()
						else:
							_Exercise = Exercise(Type = x[0], Level = Level_Num, Name = _Name, Code = Input_Code)
							_Exercise.save()
		return HttpResponseRedirect("/admin-exercises")

	context["Exercises_1"] = LG_1_Exercises[0]
	context["Exercises_2"] = LG_1_Exercises[1]
	context["Exercises_3"] = LG_1_Exercises[2]

	# context["Levels"] = [[1, []],[2, []],[3, []],[4, []],[5, []]]

	Exercises_List_1 = []

	for i in Exercise.objects.all():
		row = []
		row.append(i.Type)
		row.append(i.Level)
		row.append(i.Name)
		row.append(i.Bodyweight)
		# print(row)
		Exercises_List_1.append(row)


	return render(request, "admin_exercises.html", context)

def Admin_Users(request): 
	context = {}
	context["Users"] = []
	for _User in User.objects.all():
		_Member = Member.objects.get(User=_User)
		row = []
		row.append(_User.username)
		row.append(_User.pk)
		row.append(_User.first_name)
		row.append(_User.last_name)
		context["Users"].append(row)
	if request.method == 'GET':
		print("GET REQUEST RECEIVED")
	if request.method == 'POST':
		print("POST REQUEST RECEIVED")
		keys = []
		for i in request.POST.keys():
			keys.append(i)
			print(i)
			print(type(i))
			print(len(i))
			if len(i) < 4:
				request.session["User_PK"] = str(i)
		print("POST REQUEST RECEIVED")
		return HttpResponseRedirect("/admin-users-view-profile/")
	return render(request, "admin_users.html", context)


def Admin_User_Profile (request):
	User_PK = int(request.session["User_PK"])
	_User = User.objects.get(pk=User_PK)
	_Member = Member.objects.get(User=_User)
	_Workouts = _Member.workouts.all()
	_Now = datetime.now()
	_Past_Times = []
	_Future_Times = []
	print("From Admin User Profile: " + str(User_PK))
	print("Current Time: " + str(datetime.now()))
	context = {}
	context["User_Info"] = []
	context["User_Info"].append(_User.username)
	context["User_Info"].append(_User.first_name)
	context["User_Info"].append(_User.last_name)
	context["User_Info"].append(_Member.Level)
	for i in _Workouts:
		_Datetime = datetime.strptime(i._Date, '%m/%d/%Y')
		i.Date = _Datetime.date()
		i.save()
		# print(str(i) + " " + i._Date + " " + str(datetime.strptime(i._Date, '%m/%d/%Y')))
		print(str(i) + " " + i._Date + " " + str(i.Date))
		if _Datetime >_Now:
			_Distance = _Datetime - datetime.now()
			_Future_Times.append(_Distance)
			if _Distance <= min(_Future_Times):
				Next_Workout = i
		elif _Datetime < _Now:
			_Distance = datetime.now() - _Datetime
			_Past_Times.append(_Distance)
			if _Distance <= min(_Past_Times):
				Last_Workout = i
	print(_Future_Times)
	print(_Past_Times)
	context["Next_Workout"] = []
	context["Last_Workout"] = []
	if _Future_Times:
		print("Future Min Time: " + str(min(_Future_Times)))
		print("Next Workout: " + str(Next_Workout) + " " + Next_Workout._Date)
		_Summary = ", Level " + str(Next_Workout.Level) + " Week " + str(Next_Workout.Week) + " Day " + str(Next_Workout.Day)
		context["Next_Workout"].append(_Summary)
		context["Next_Workout"].append(Next_Workout._Date)
		_Subs = []
		for _sub in Next_Workout.SubWorkouts.all():
			_Description = str(_sub.Sets) + " x " + str(_sub.Reps) + " " + _sub.Exercise.Name
			_Subs.append(_Description)
		context["Next_Workout"].append(_Subs)
	else:
		context["Next_Workout"].append("None")		
	if _Past_Times:
		print("Past Min Time: " + str(min(_Past_Times)))
		print("Last Workout: " + str(Last_Workout) + " " + Last_Workout._Date)	
		_Summary = ", Level " + str(Last_Workout.Level) + " Week " + str(Last_Workout.Template.Week) + " Day " + str(Last_Workout.Template.Day)
		context["Last_Workout"].append(_Summary)
		context["Last_Workout"].append(Last_Workout._Date)
		_Subs = []
		for _sub in Last_Workout.SubWorkouts.all():
			_Description = str(_sub.Sets) + " x " + str(_sub.Reps) + " " + _sub.Exercise.Name
			_Subs.append(_Description)
		context["Last_Workout"].append(_Subs)
	else:
		context["Last_Workout"].append("None")

	return render(request, "admin_user_profile.html", context)

def Admin_Videos(request):
	context = {}
	context["Video_Display"] = []
	context["Video_Display_Test"] = ["videos/Dashboard_Shot.png", 1]
	context["Exercise_Types"] = ["UB Hor Push", "Hinge", "Squat", "UB Vert Push",  "UB Hor Pull", "UB Vert Pull",  "LB Uni Push", 
	"Ant Chain", "Post Chain",  "Isolation", "Iso 2", "Iso 3", "Iso 4", "RFL Load", "RFD Unload 1", "RFD Unload 2"]
	context["Levels"] = Levels
	context["Level_Display"] = []
	# context[""]
	if "Current_Exercises" not in request.session.keys():
		request.session["Current_Exercises"] = []

	for i in Video.objects.all():
		# i.delete()
		row = []
		_Type = i.Exercise_Type
		_Image_URL = "/" + i.File.url
		_Thumbnail_URL = "/" + i.Thumbnail.url
		row.append(i.Title)
		_Name = i.File.name.replace("static/videos/", "")
		print("File Name: " + i.File.name)
		print("File URL: " + i.File.url)
		_URL = i.File.url.replace("static/", "")
		# row.append(_URL)
		row.append(_URL)
		row.append("videos/Dashboard_Shot.png")
		row.append(i.File.url)
		row.append(_Image_URL)
		row.append(_Thumbnail_URL)
		row.append(_Type)
		Exercise_Names = []
		for x in i.exercises.all():
			Exercise_Names.append(x)
		row.append(Exercise_Names)
		context["Video_Display"].append(row)

	if request.method == "POST":
		Selected_Exercise = request.POST['Exercise']
		print(request.POST['Exercise'])
		request.session["Exercise"] = request.POST['Exercise']
		# return HttpResponseRedirect("/admin-videos")

	if request.POST.get("Clear"):
		for i in Video.objects.all():
			i.delete()
		return HttpResponseRedirect("/admin-videos")

	# if request.POST.get("Level"):
	# 	print("LEVEL SELECTED: " + request.POST['Level'])
	# 	request.session["Level"] = int(request.POST['Level'])

	if "Exercise" in request.session.keys():
		_Type = request.session['Exercise']
		context["Selected_Exercise"] = [_Type]
		# context["Exercise_Types"] = Exercise_Types
		context["Exercise_Types"].remove(_Type)

		print("Selected Exercise: " + request.session['Exercise'])
		_Exercises = Exercise.objects.filter(Type = _Type)
		for n in Levels:
			if Exercise.objects.filter(Type = _Type, Level = n).exists():
				_Exercise = Exercise.objects.get(Type=_Type, Level = n)
				context["Level_Display"].append([str(n) + " (" + _Exercise.Name + ")", _Exercise.Name])
	else:
		context["Level_Display"] = Levels

	# if request.POST.get("Exercise"):
	# 	print("EXERCISE SELECTED: " + request.POST['Exercise'])
	# 	request.session["Exercise"] = request.POST['Exercise']
	# 	return HttpResponseRedirect("/admin-videos")

	# if request.method == "POST":
	# 	print(request.POST['Level'])

	if request.POST.get("AddExercises"):
		print("AddExercises Pressed")
		Add_Exercises = request.POST.getlist("Exercise_List")
		for i in Add_Exercises:
			if i not in request.session["Current_Exercises"]:
				request.session["Current_Exercises"].append(i)
		print("Add Exercises: " + str(Add_Exercises))

	context["Current_Exercises"] = request.session["Current_Exercises"]

	if request.POST.get("VideoUploadSubmit"):
		# cwd = os.getcwd()
		# print(str(request.GET.get("VideoUpload")))
		# _File = request.GET.get("VideoUpload")
		_F = request.FILES['VideoUpload']
		print("_F: " + str(_F.name))
		_File = File(_F)
		print("File: " + str(_File.name))
		_Video = Video(Title="Test")
		_Video.File = _File
		_Video.save()		

		# _File = File(open(request.POST.get("VideoUpload"), 'w+'))	
		# print(_File.name)
		# print("Upload button pressed. File Name: " + _File.name)
		return HttpResponseRedirect("/admin-videos")

	if request.POST.get("AddVideo"):
		_Title = request.POST.get("Title")
		_File = File(request.FILES['VideoUpload'])
		_Thumbnail = File(request.FILES['Thumbnail'])
		_Type = request.POST['Exercise']
		_Tags = request.POST['Tags']

		_Description = request.POST['Description']
		print(_Description)

		print(_Title)
		_Video = Video(Title = _Title, File = _File, Thumbnail = _Thumbnail, Exercise_Type=_Type, Description=_Description, Tags=_Tags)
		Add_Exercises = request.POST.getlist("Exercise_List")
		_Video.save()
		for i in Add_Exercises:
			_Exercise = Exercise.objects.get(Name = i)
			_Exercise.Video = _Video
			_Exercise.save()
		request.session["Uploading_Video_PK"] = _Video.pk

		return HttpResponseRedirect("/admin-videos-2")
	return render(request, "adminvideos.html", context)

def Admin_Videos_2(request):
	context = {}
	_Video = Video.objects.get(pk=request.session["Uploading_Video_PK"])
	_Thumbnail_URL = "/" + _Video.Thumbnail.url
	_Video_URL = "/" + _Video.File.url
	_Title = _Video.Title
	_Exercises = _Video.exercises.all()

	context["Video_Title"] = _Title
	context["Thumbnail_URL"] = _Thumbnail_URL
	context["Video_URL"] = _Video_URL
	context["Assigned_Exercises"] = []

	for i in _Exercises:
		context["Assigned_Exercises"].append([i.Name, i.Video_Description])

	if request.POST.get("UpdateDescriptions"):
		for i in _Exercises:
			if request.POST["Description" + i.Name] != "":
				i.Video_Description = request.POST["Description" + i.Name]
				i.save()
		return HttpResponseRedirect("admin-videos-2")

	# if request.POST.get("Submit_Btn"):
	# 	return HttpResponseRedirect("admin-videos-library")

	return render(request, "adminvideos2.html", context)


def Admin_Videos_Library(request):
	context = {}
	context["Videos"] = []

	for v in Video.objects.all():
		row = []
		_Exercises = v.exercises.all()
		exercises_row = []
		for i in _Exercises:
			exercises_row.append(i.Name)
		_Thumbnail_URL = "/" + v.Thumbnail.url
		row.append(_Thumbnail_URL)
		row.append(v.Title)
		row.append(v.pk)
		row.append("Edit" + v.Title + str(v.pk)) #3 is button code
		_Tags = v.Tags.split(',')
		Tags = ""
		for _Tag in _Tags:
			Tags = Tags + " , " + _Tag
		row.append(Tags) #4 is tags
		row.append(exercises_row) #5 is exercises
		context["Videos"].append(row)

	if request.method == 'POST':
		# for key in request.GET:
		# 	print("Request Object: " + request.GET[key])
		Keys = []
		for i in request.POST.keys():
			Keys.append(i)
			# print("Key: " + i)
			# print("Key: " + i)
			# print(type(i))
			# if i is int:
			# 	print("Int Key: " + i)
			# if i is str:
			# 	print("String Key: " + i)
				# print("Request Value: " + request.POST[i])
				# request.session["Video_PK"] = int(i)
		# print(request.GET)
		print("First Key: " + Keys[0])
		print("Second Key: " + Keys[1])
		print("REQUEST RECEIVED: ")
		request.session["Video_PK"] = int(Keys[1])
		return HttpResponseRedirect("/admin-videos-library-edit")
	return render(request, "adminvideoslibrary.html", context)

def Admin_Videos_Edit(request):
	context = {}
	_Video = Video.objects.get(pk=request.session["Video_PK"])
	_Type = _Video.Exercise_Type
	_Exercise_List = Exercise.objects.filter(Type=_Type)
	_Assigned_Exercises = _Video.exercises.all()
	context["Display"] = []
	_Thumbnail_URL = "/" + _Video.Thumbnail.url
	_Video_URL = "/" + _Video.File.url

	context["Display"].append(_Thumbnail_URL) 
	context["Display"].append(_Video.Exercise_Type)
	context["Exercise_Types"] = Exercise_Types
	context["Exercise_List"] = []
	context["Assigned_Exercises"] = []
	context["Video_URL"] = _Video_URL

	# print("Test")
	# print("PK from Edit: " + str(request.session["Video_PK"]))
	for i in _Exercise_List:
		row = []
		row.append(i.Name)
		row.append(i.Level)
		row.append(i.pk)
		context["Exercise_List"].append(row)
	for i in _Assigned_Exercises:
		row = []
		row.append(i.Name)
		row.append(i.Level)
		row.append(i.pk)
		context["Assigned_Exercises"].append(row)

	if request.GET.get("RemoveExercises"):
		PKs = request.GET.getlist("Remove_Exercises")
		for i in PKs:
			_Exercise = Exercise.objects.get(pk=i)
			print(_Exercise.Name)
			_Exercise.Video = None
			_Exercise.save()
		return HttpResponseRedirect('/admin-videos-library-edit')

	if request.GET.get("AddExercises"):
		print("Test Submit")
		PKs = request.GET.getlist("Assign_Exercises")
		print(PKs)
		for i in PKs:
			print(i)
			_Exercise = Exercise.objects.get(pk=i)
			print(_Exercise.Name)
			_Exercise.Video = _Video
			_Exercise.save()
		return HttpResponseRedirect('/admin-videos-library-edit')

	return render(request, "adminvideosedit.html", context)
