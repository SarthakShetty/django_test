from models import *
def Feature3_create_new_user(name, age, phone_number,password, date_creation=None, photo_url=None):
	create_new_user(name, int(age), phone_number,password)

def sign_in(phone_number,password):
	x=User.objects.get(phone_number=phone_number)
	if x:
		if password==x.password:
			return True
		else:
			return False
	return False	

def Feature3_create_new_group(name, destination, date_creation):
	g_id = create_new_group(name, destination, date_creation)
	return HttpResponse(g_id)


def Feature3_add_members_to_group(g_id, phone_number_list):
	invalid_phone_numbers = add_members_to_group(int(g_id), phone_number_list)
	return HttpResponse(invalid_phone_numbers)


def Feature3_make_admin(g_id, phone_number ):
	make_admin(int(g_id), phone_number)
	return HttpResponse("Success")


def Feature3_send_message_to_group(phone_number, g_id, video_url, photo_url, text):
	send_message_to_group(phone_number, int(g_id), video_url, photo_url, text)
	return HttpResponse("Success")


def Feature3_get_member_coordinates(g_id):
	L = get_member_coordinates(int(g_id))
	return HttpResponse(L)


def Feature3_is_user_in_group(phone_number):
	status = is_user_in_group(phone_number)
	return HttpResponse(status)


def Feature3_delete_group(phone_number):
	delete_group(phone_number)
	return HttpResponse("Success")

def Feature3_update_user_location(phone_number, latitude, longitude):
	update_user_location(phone_number, float(latitude), float(longitude))
	return HttpResponse("Success")
