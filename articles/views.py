from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.core import serializers
from django.template import Context
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import json
#from models import *
import roundabout
import freestyle
import functions

# feature 4 imports
from random import shuffle
from random import randrange
from django.utils import timezone
from queries import on_start_trip, on_finish_trip, check_in, display_trip_details, view_trips, check_if_trip_exists, insert_review, get_places
from gen_diary import get_diary


@csrf_exempt
def Feature2(request):
	if request.method=="POST":
		l = request.body.split("::")
		no_users=len(l)-1
		if no_users>2:
			location = l[0:1]+l[2:]
		else:
			location = l[0]
		radius = l[1][0:-2]
		json_places = roundabout.feature2(location,int(radius)*1000,no_users)
		return HttpResponse(json.dumps(json_places))
	
@csrf_exempt
def Feature1_Module2(request):
    data = request.body[1:-1].split(",")
    final_dict = freestyle.get_best_route(data[0], data[1], data[2:])# Goes into Feature1_Module2
    json_dict = json.dumps(final_dict, sort_keys=True,indent=4, separators=(',', ': '))
    return HttpResponse('{ "route" :[' + json_dict + "\n]}")


@csrf_exempt
def Feature1_Module1(request):
    data = request.body.split("::")
    full_dict = freestyle.get_points_of_interest(data[0], data[1])  # Goes into Feature1_Module1
    json_str = json.dumps(full_dict, sort_keys=True,indent=4, separators=(',', ': '))
    return HttpResponse(json_str)


'''
Feature4 Views
'''

# input_dict={"Op":"7","phoneNumber":"hello","tripId":5,"placeName":"mumbai"}
# : was used for testing
import json
import re
try:
    import urllib2
except:
    print("Run with python2")


@csrf_exempt
def index(request):
	output_dict = {}
	print request.body
	if request.method == 'POST':
		input_dict = json.loads(request.body)
        op_code = input_dict["Op"]
        if op_code == "1":
            phone_number = input_dict["phNo"]

            trip_id = on_start_trip(phone_number)
            print trip_id
            output_dict["Op"] = op_code
            output_dict["trip_id"] = trip_id
            print output_dict
            return HttpResponse(json.dumps(output_dict))

        elif op_code == "2":
            place_name = input_dict["placeName"]
            trip_id = input_dict["tripId"]
            check_in(place_name, trip_id)
            output_dict["Op"] = op_code
            return HttpResponse(json.dumps(output_dict))

        elif op_code == "3":
            trip_id = input_dict["tripId"]
            d = {}
            d = display_trip_details(trip_id)
            # startTime=d["startTime"]
            count = d["count"]
            output_dict["Op"] = op_code
            # output_dict["startTime"]=startTime
            output_dict["count"] = count
            return HttpResponse(json.dumps(output_dict))

        elif op_code == "4":
            # gen diary
            phone_number = input_dict["phNo"]
            trip_id = input_dict["tripId"]
            on_finish_trip(trip_id, phone_number)
            # gen diary

            trip_id = input_dict["tripId"]
            places = get_places(trip_id)
            trip_review = get_diary(places)

            insert_review(trip_id, trip_review)
            output_dict["Op"] = op_code
            output_dict["review"] = trip_review
            # output_dict["places"]=places
            return HttpResponse(json.dumps(output_dict))

        elif op_code == "5":
            phone_number = input_dict["phNo"]
            d = {}
            d = view_trips(phone_number)
            output_dict["Op"] = op_code
            output_dict["Trips"] = d
            return HttpResponse(json.dumps(output_dict))

        elif op_code == "6":
            trip_id = input_dict["tripId"]
            phone_number = input_dict["phNo"]
            c = check_if_trip_exists(trip_id, phone_number)
            if c:
                d = {}
                d = display_trip_details(trip_id)
                # startTime=d["startTime"]
                count = d["count"]
                output_dict["Op"] = op_code
                # output_dict["startTime"]=startTime
                output_dict["count"] = count
                return HttpResponse(json.dumps(output_dict))
            else:
                output_dict["Op"] = op_code
                output_dict["count"] = -1
                return HttpResponse(json.dumps(output_dict))

        elif op_code == "7":
            # gen diary

            trip_id = input_dict["tripId"]
            places = get_places(trip_id)
            trip_review = get_diary(places)

            insert_review(trip_id, trip_review)
            output_dict["Op"] = op_code
            output_dict["review"] = trip_review
            # output_dict["places"]=places
            return HttpResponse(json.dumps(output_dict))


def login(request):
	input_dict = json.loads(request.body)
	op = int(input_dict["op"])
	if op==0:
		name = input_dict["name"]
		pwd = input_dict["password"]
		phone = input_dict["phone"]
		age = input_dict["age"]
		try:
			functions.Feature3_create_new_user(name,int(age),phone)
		except IntegrityError:
			return HttpResponse("There is an account associated with this number.")
		except:
			return HttpResponse("Unknown error.")
	elif op==1:
		phone = input_dict["phone"]
		pwd = input_dict["password"]
		if functions.sign_in(phone,pwd):
			return HttpsResponse("success")
		
		
		
def group_activity(request):
	input_dict = json.loads(request.body)
	op = int(input_dict["op"])
	if op==0:
		
		
