from django.core import serializers
from django.http import *
from django.shortcuts import render
from django.template import Context
from django.template import RequestContext
from django.template.loader import get_template
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from models import *
from random import randrange
from random import shuffle
from gen_diary import get_diary
from queries import (on_start_trip, on_finish_trip, 
        check_in, display_trip_details, view_trips, 
        check_if_trip_exists, insert_review, get_places)
import datetime
import freestyle
import json
import re
import roundabout
try:
    import urllib2
except:
    print("Run with python2")

''' ============ Non-feature related views ============ '''

@csrf_exempt
def homepage(request):
    now = datetime.datetime.now()
    html = """<!doctype html><html><body><h3>Welcome to EGM's backend Django server! <br><br>It is now %s. </h3> """  % now + """

<h4> Views for feature 1 (that should be implemented but haven't) <h4>
<pre>
@csrf_exempt
def freestyle_getroute(request):
    ''' Get source, destination, and some points of interest. Return an optimal route json for rendering at the front end '''
    exec("source  = request.%s['source']" %request.method)
    exec("dest    = request.%s['dest']" %request.method)
    exec("json_waypoints    = json.loads(request.%s['json_waypoints'])" %request.method)
    #json_waypoints = request.body
    optimal_route = freestyle.get_best_route(source, dest, json_waypoints)

    return HttpResponse(json.dumps(optimal_route, indent=4), content_type="application/json")

@csrf_exempt
def freestyle_getpoints(request):
    ''' Get source and destination from user, and return points of interest '''
    exec("source  = request.%s['source']" %request.method)
    exec("dest    = request.%s['dest']" %request.method)

    points_of_interest = freestyle.get_points_of_interest(source, dest)
    return HttpResponse(json.dumps(points_of_interest, indent=4))
    </pre>
</body></html>"""

    return HttpResponse(html)

''' ============ Feature 1 ============ '''

@csrf_exempt
def Feature1_Module1(request):
    data = request.body.split("::")
    full_dict = freestyle.get_points_of_interest(data[0], data[1])  # Goes into Feature1_Module1
    json_str = json.dumps(full_dict, sort_keys=True,indent=4, separators=(',', ': '))
    return HttpResponse(json_str)

@csrf_exempt
def Feature1_Module2(request):
    data = request.body[1:-1].split(",")
    final_dict = freestyle.get_best_route(data[0], data[1], data[2:])# Goes into Feature1_Module2
    json_dict = json.dumps(final_dict, sort_keys=True,indent=4, separators=(',', ': '))
    return HttpResponse('{ "route" :[' + json_dict + "\n]}")

''' ============ Feature 2 ============ '''

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
    
''' ============ Feature 4 ============ '''

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

''' ============ Feature 3 ============ '''

def Feature3_create_new_user(request):
    if request.method == "POST":
        name, age, phone_numbsser, date_creation, photo_url = request.body.split(
            "::")
        create_new_user(name, int(age), phone_number, date_creation, photo_url)
        return HttpResponse("Success")


def Feature3_create_new_group(request):
    if request.method == "POST":
        name, destination, date_creation = request.body.split("::")
        g_id = create_new_group(name, destination, date_creation)
        return HttpResponse(g_id)


def Feature3_add_members_to_group(request):
    if request.method == "POST":
        g_id, phone_number_list = request.body.split("::")
        invalid_phone_numbers = add_members_to_group(
            int(g_id), phone_number_list)
        return HttpResponse(invalid_phone_numbers)


def Feature3_make_admin(request):
    if request.method == "POST":
        g_id, phone_number = request.body.split("::")
        make_admin(int(g_id), phone_number)
        return HttpResponse("Success")


def Feature3_send_message_to_group(request):
    if request.method == "POST":
        phone_number, g_id, video_url, photo_url, text = request.body.split(
            "::")
        send_message_to_group(phone_number, int(
            g_id), video_url, photo_url, text)
        return HttpResponse("Success")


def Feature3_get_member_coordinates(request):
    if request.method == "POST":
        g_id = request.body
        L = get_member_coordinates(int(g_id))
        return HttpResponse(L)


def Feature3_is_user_in_group(request):
    if request.method == "POST":
        phone_number = request.body
        status = is_user_in_group(phone_number)
        return HttpResponse(status)


def Feature3_delete_group(request):
    if request.method == "POST":
        phone_number = request.body
        delete_group(phone_number)
        return HttpResponse("Success")


def Feature3_update_user_location(request):
    if request.method == "POST":
        phone_number, latitude, longitude = request.body.split("::")
        update_user_location(phone_number, float(latitude), float(longitude))
        return HttpResponse("Success")
