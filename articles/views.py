from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.core import serializers
from django.template import Context
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import json
from freestyle_module_1 import *
from freestyle_module_2 import *
import roundabout

#feature 4 imports
from random import shuffle
from random import randrange
from django.utils import timezone
from queries import on_start_trip,on_finish_trip,check_in,display_trip_details,view_trips,check_if_trip_exists,insert_review,get_places
from gen_diary import get_diary


data=[]
full_dict =  dict()
result_dict = dict()
final_dict=dict()
json_str = ""
json_dict = ""

def getPlaces(data):
	global full_dict
	global result_dict
	#print full_dict
	for i in data:
		if(i in full_dict.keys()):
			result_dict[i] = full_dict[i]
@csrf_exempt
def Feature2(request):
	if request.method=="POST":
		l = request.body.split("::")
		location = l[0]
		radius = l[1][0:-2]
		json_places = roundabout.feature2(location,int(radius)*1000)
		print json_places
		return HttpResponse(json.dumps(json_places))
	
@csrf_exempt
def Feature1_Module2(request):
 	global final_dict
 	global json_dict
 	global result_dict
 	if request.method=="GET":
 	    print '--------------------GET--------------------'
 	    json_dict =json.dumps(final_dict,sort_keys=True,indent=4,separators=(',',': ')) 
 	    print '--------------------GET--------------------'
 	    print '\n\n'
 	    return HttpResponse('{ "route" :['+  json_dict+ "\n]}") #Back to front end
 	else:
 	    print '--------------------POST--------------------'
 	    data =  request.body[1:-1].split(",")
 	    #data = [x.strip(' ') for x in data]
 	    #print data
 	    getPlaces(data[2:])
 	    #print result_dict
 	    final_dict = run(data[0],data[1],result_dict)  #Goes into Feature1_Module2
 	    print '--------------------POST--------------------'
 	    print '\n\n'
 	    return HttpResponse(data)

@csrf_exempt	
def Feature1_Module1(request):
	global full_dict
	global json_str
	if request.method=="GET":
		print '--------------------GET--------------------'
		print '--------------------GET--------------------'
		print '\n\n'
		return HttpResponse(json_str) #Back to front end
	else:
		print '--------------------POST--------------------'
		data =  request.body.split("::")
		print data[0],'\n',data[1]
		#print full_dict
		full_dict = get_points_of_interest(data[0],data[1]) #Goes into Feature1_Module1
		json_str = json.dumps(full_dict,sort_keys=True,indent=4,separators=(',',': '))
		print '--------------------POST--------------------'
		print '\n\n'
		return HttpResponse("Success")
		
		

'''
Feature4 Views
'''

input_dict={"Op":"7","phoneNumber":"hello","tripId":5,"placeName":"mumbai"}
import json
import re
try:
    import urllib2
except:
    print("Run with python2")
output_dict={}
def index(request):
	if request.method == 'GET':
		#input_dict=json.loads(request.body);
		op_code=input_dict["Op"]
		if op_code=="1":
			phone_number=input_dict["phoneNumber"]
			
			trip_id=on_start_trip(phone_number)
			output_dict["Op"]=op_code
			output_dict["trip_id"]=trip_id
			return HttpResponse(json.dumps(output_dict))
		
		elif op_code=="2":
			place_name=input_dict["placeName"]
			trip_id=input_dict["tripId"]
			check_in(place_name,trip_id)
			output_dict["Op"]=op_code
			return HttpResponse(json.dumps(output_dict))
		
		elif op_code=="3":
			trip_id=input_dict["tripId"]
			d={}
			d=display_trip_details(trip_id)
			#startTime=d["startTime"]
			count=d["count"]
			output_dict["Op"]=op_code
			#output_dict["startTime"]=startTime
			output_dict["count"]=count
			return HttpResponse(json.dumps(output_dict))
		
		elif op_code=="4":
			#gen diary
			phone_number=input_dict["phoneNumber"]
			trip_id=input_dict["tripId"]
			on_finish_trip(trip_id,phone_number)
			output_dict["Op"]=op_code
			return HttpResponse(json.dumps(output_dict))
			
		elif op_code=="5":
			phone_number=input_dict["phoneNumber"]
			d={}
			d=view_trips(phone_number)
			output_dict["Op"]=op_code
			output_dict["Trips"]=d
			return HttpResponse(json.dumps(output_dict))
			
		elif op_code=="6":
			trip_id=input_dict["tripId"]
			phone_number=input_dict["phoneNumber"]
			c=check_if_trip_exists(trip_id,phone_number)
			if c:
				d={}
				d=display_trip_details(trip_id)
				#startTime=d["startTime"]
				count=d["count"]
				output_dict["Op"]=op_code
				#output_dict["startTime"]=startTime
				output_dict["count"]=count
				return HttpResponse(json.dumps(output_dict))
			else:
				output_dict["Op"]=op_code
				output_dict["count"]=-1
				return HttpResponse(json.dumps(output_dict))
				
		elif op_code=="7":
			#gen diary
			
			trip_id=input_dict["tripId"]
			places=get_places(trip_id)
			trip_review=get_diary(places)
			
			insert_review(trip_id,trip_review)
			output_dict["Op"]=op_code
			output_dict["review"]=trip_review
			#output_dict["places"]=places
			return HttpResponse(json.dumps(output_dict))
