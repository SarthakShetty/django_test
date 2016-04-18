from dt.models import User,Places,Trip,PlacesInTrip,UserTrips
from django.utils import timezone
def on_start_trip(phone_number):
		#Insert into trip table - trip_start_datetime
		Trip.objects.create(trip_start_datetime=timezone.now())
		trip_id=Trip.objects.count()	#to get the trip_id,which will be the maximum one
		p=User.objects.get(phone_number=phone_number)
		t=Trip.objects.get(trip_id=trip_id)
		UserTrips.objects.create(phone_number=p,trip_id=t)
		return trip_id
	
def on_finish_trip(trip_id,phone_number):
	try:	#update Trip table
		Trip.objects.filter(trip_id=trip_id).update(trip_end_datetime=timezone.now())
	except:
		raise Exception("Couldn't update Trip table")
def check_in(place_name,trip_id):
	
		t=Places.objects.filter(place_name=place_name)[0]
		if not t:	#if the place doesnt exist,insert the place into the place table
			p=Places.objects.create(place_name=place_name)
			place_id=p.place_id
		else:
			place_id=t.place_id
		t=Trip.objects.get(trip_id=trip_id)
		p=Places.objects.get(place_id=place_id)
		PlacesInTrip.objects.create(trip_id=t,place_id=p,place_checkin_datetime=timezone.now())
	
		
def display_trip_details(trip_id):
	try:
		d={}
		places=PlacesInTrip.objects.filter(trip_id=trip_id)
		count=len(places)
		startTime=Trip.objects.get(trip_id=trip_id).trip_start_datetime
		d['count']=count
		d['startTime']=startTime
		return d
	except:
		raise Exception("Couldn't return trip details of the trip with id : "+trip_id)
		
def view_trips(phone_number):	#all the trips visited by the user
	try:
		c=UserTrips.objects.filter(phone_number=phone_number)
		if c:
			d={}
			for i in c:
				t1=i.trip_id
				t=str(t)
				d[t]=Trip.objects.get(trip_id=t).trip_review
			return d
	except:
		raise Exception("No user with : "+phone_number);

def check_if_trip_exists(trip_id,phone_number):
	try:
		check=UserTrips.objects.filter(trip_id=trip_id,phone_number=phone_number)
		if check:
			return 1
		else:
			return -1
	except:
		raise Exception("Couldnt check")
			
def insert_review(trip_id,trip_review):
	try:
		Trip.objects.filter(trip_id=trip_id).update(trip_review=trip_review)
	except:
		raise Exception("Couldn't add trip review for trip with id : "+trip_id)
		
def get_places(trip_id):
	try:
		f=PlacesInTrip.objects.filter(trip_id=trip_id)
		places=[]
		for i in f:
			places.append(i.place_id.place_name)
		return places
	except:
		raise Exception("Couldnt return places")
			
		


	
		
	
	
	
