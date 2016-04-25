from models import *
def Feature3_create_new_user(name, phone_number,password,regid, date_creation=None, photo_url=None):
	create_new_user(name, phone_number,password,regid)

def sign_in(phone_number,password):
	try:
		x=User.objects.get(phone_number=phone_number)
	except:
		return 2
	if x:
		if password==x.password:
			if x.session_id ==1:
				return 4
			x.session_id =1
			x.save()
			return x.session_id
		else:
			return 3
	

def sign_out(phone_number):
	x=User.objects.get(phone_number=phone_number)
	if x.session_id==1:
		x.session_id=0		
		x.save()
		return "Signed Out"
	return "Need to be signed in to sign out."



