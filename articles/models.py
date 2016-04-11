'''
user(phone_number(pkey),age,name,photo_url,date_creation)
group(g_id(pkey),name,date_creation, destination)
group_message(gm_id(pkey),video_url,photo_url,text)
user_is_admin_group(g_id(pkey)(fkey from group),phone_number(fkey from user))
user_is_group_member(g_id(pkey)(fkey from group),phone_number(pkey)(fkey from user))
user_send_group_message(phone_number(pkey)(fkey from user),gm_id(pkey)(fkey from group_message),g_id(fkey from group))
user_receives_group_message(phone_number(pkey)(fkey from user),gm_id(pkey)(fkey from group_message),g_id(fkey from group))
places(place_id(pkey), place_name, place_geo_location, place_description, place_reviews)
places_in_trip(trip_id(pkey)(fkey from trip), place_id(pkey)(fkey references from places), place_checkin_datetime)
trip(trip_id(pkey), trip_review, trip_start_datetime, trip_end_datetime)
user_trips(phone_number(pkey)(fkey from user), trip_id(pkey)(fkey from trips))
'''

from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
import datetime

invalid_phone_numbers=[]

class User(models.Model):
    phone_number = models.CharField(max_length=10, primary_key=True) #Given by the user
    age = models.IntegerField()
    name = models.CharField(max_length=50)
    photo_url = models.URLField(max_length=100)
    date_creation = models.DateTimeField(default=timezone.now)


class Group(models.Model):
	g_id = models.AutoField(primary_key=True) #Not given by the user, Automatically assigned to user and incremented
	name = models.CharField(max_length=25)
	date_creation = models.DateTimeField(default=timezone.now)
	destination = models.CharField(max_length=50)
	

class GroupMessage(models.Model):
	gm_id = models.AutoField(primary_key=True) #Not given by the user, Automatically assigned to user and incremented
	video_url = models.URLField(max_length=100)
	photo_url = models.URLField(max_length=100)
	text = models.CharField(max_length=500)


class UserIsAdminGroup(models.Model):
	g_id = models.OneToOneField('group', on_delete=models.CASCADE)
	phone_number = models.OneToOneField('user', on_delete=models.CASCADE)
	
	class Meta:
	    unique_together = ("g_id", "phone_number")


class UserIsGroupMember(models.Model):
	g_id = models.OneToOneField('group', on_delete=models.CASCADE)
	phone_number = models.OneToOneField('user', on_delete=models.CASCADE)
	latitude = models.FloatField()
	longitude = models.FloatField()
	
	class Meta:
	    unique_together = ("g_id", "phone_number")


class UserSendsGroupMessage(models.Model):
    phone_number = models.OneToOneField('User', on_delete=models.CASCADE)
    gm_id = models.OneToOneField('Group_message', on_delete=models.CASCADE)
    g_id = models.OneToOneField('Group', on_delete=models.CASCADE)
    
    class Meta:
	    unique_together = ("phone_number", "gm_id")


class UserReceivesGroupMessage(models.Model):
    phone_number = models.OneToOneField('User', on_delete=models.CASCADE)
    gm_id = models.OneToOneField('Group_message', on_delete=models.CASCADE)
    g_id = models.OneToOneField('Group', on_delete=models.CASCADE)
    
    class Meta:
	    unique_together = ("phone_number", "gm_id")
	

class Places(models.Model):
	place_id = models.CharField(max_length=100, primary_key=True)
	place_name = models.CharField(max_length=100)
	place_geo_location = models.CharField(max_length=100)
	place_description = models.CharField(max_length=1000)
	place_reviews = models.CharField(max_length=1000)


class Trip(models.Model):
	trip_id = models.AutoField(primary_key=True)
	trip_review = models.CharField(max_length=1000)
	trip_start_datetime = models.DateTimeField(default=timezone.now)
	trip_end_datetime = models.DateTimeField(default=timezone.now)


class PlacesInTrip(models.Model):
	trip_id = models.OneToOneField('Trip', on_delete=models.CASCADE)
	place_id = models.OneToOneField('Places', on_delete=models.CASCADE)
	place_checkin_datetime = models.DateTimeField(default=timezone.now)
	
	class Meta:
	    unique_together = ("trip_id", "place_id")


class UserTrips(models.Model):
	phone_number = models.OneToOneField('User',on_delete=models.CASCADE)
	trip_id = models.OneToOneField('Trip',on_delete=models.CASCADE)
	
	class Meta:
	    unique_together = ("phone_number", "trip_id")


def create_new_user(name, age, phone_number, date_creation=None, photo_url=None):
	if date_creation == None: 
		date_creation = timezone.now
	try:
		User.objects.create(name=name, age=age, phone_number=phone_number, date_creation=date_creation, photo_url=photo_url)
	
	except:
		raise Exception("Error during creating user")


def create_new_group(name, destination, date_creation=None):
	if date_creation == None: 
		date_creation = timezone.now
	try:
		return Group.objects.create(name=name, date_creation=date_creation, destination=destination).g_id  # create the table entry and then return g_id to the front end

	except:
		raise Exception("Error during creating group")


def add_members_to_group(g_id, phone_number_list):
	try:
		invalid_phone_numbers.clear()
		
		for phone_number in phone_number_list:
			add_member_to_group(g_id, phone_number)
		
		if len(invalid_phone_numbers) == 0: 
			return True
		
		return invalid_phone_numbers
		
	except:
		raise
		

def add_member_to_group(g_id, phone_number):
	try:
		User.objects.get(phone_number=phone_number) 
		UserIsGroupMember.objects.create(g_id=g_id, phone_number=phone_number)
	
	except ObjectDoesNotExist:
		invalid_phone_numbers.append(phone_number)
	
	except:
		raise Exception("Error during adding " +str(phone_number) + " to group " + str(g_id))


def make_admin(g_id, phone_number):
	''' This function will remove the existing admin to create a new admin '''
	try:
		AdminEntry, isNewEntry = UserIsGroupMember.objects.get_or_create(g_id=g_id, default={'phone_number': phone_number})
		
		if(not isNewEntry):	# if an admin has already been assigned, delete the existing entry
			tableEntry.delete()
			UserIsGroupMember.objects.create(g_id=g_id, phone_number=phone_number)

	except:
		raise Exception("Error during making " + str(phone_number) + " admin of group " + str(g_id))


def send_message_to_group(phone_number, g_id, video_url=None, photo_url=None, text=None):
	''' this function automatically handles 
		-	message creation
		-	updating the send table
		-	updating the receive table for all recipients in the group
	'''

	if video_url == None and photo_url == None and text == None:
		return

	try:	
		messageEntry = GroupMessage.objects.create(video_url=video_url, photo_url=photo_url, text=text)
	except:
		raise Exception("Error during message creation")

	try:
		UserSendsGroupMessage.objects.create(phone_number=phone_number, g_id=g_id, gm_id=messageEntry.gm_id)

	except:
		raise Exception("Error updating the table for sender")

	try:
		for tableEntry in Entry.objects.filter(g_id=g_id):
			UserReceivesGroupMessage.objects.create(phone_number=tableEntry.phone_number, g_id=g_id, gm_id=messageEntry.gm_id)

	except: 
		raise Exception("Error updating table for recipients")


def get_member_coordinates(g_id):
	try:
		L = []
		for userEntry in UserIsGroupMember.objects.filter(g_id=g_id):
			L.append( (User.objects.get(phone_number=userEntry.phone_number).name, 
				{'latitude': userEntry.latitude, 'longitude': userEntry.longitude}) )

		return L

	except:
		raise Exception("Error accessing location for group with id " + str(g_id))
		

def is_user_in_group(phone_number):
	try:
		UserIsGroupMember.objects.get(phone_number=phone_number)
		return True
	
	except ObjectDoesNotExist:
		return False


def delete_group(phone_number):
	try:
		g_id=UserIsAdminGroup.objects.get(phone_number=phone_number)
		
		Group.objects.get(g_id=g_id).delete()
		UserIsGroupMember.objects.filter(g_id=g_id).delete()
		UserIsAdminGroup.objects.get(g_id=g_id).delete()	
	
	except:
		raise Exception("Error deleting group")
		
		
def update_user_location(phone_number, latitude, longitude):
	try:
		userEntry = UserIsGroupMember.objects.filter(phone_number=phone_number) 

		userEntry.latitude, userEntry.longitude = latitude, longitude

	except:
		raise Exception("Error updating location")
	
	
	
	
		''' validate users - check phone number
		
			add users to grp - suppors list of ph nos.
		
		'''

