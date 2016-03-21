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
def hello(request):
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
def hello_template(request):
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
