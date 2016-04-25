from models import *
import requests
import json
url = "Https://gcm-http.googleapis.com/gcm/send"
headers = {'Content-Type':'application/json','Authorization':'key=AIzaSyBQZL-aILU9JbkgcjzQ20K0326v_2lq2_k'}

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


def send_message(phone,message):
	data = {};notification={};payload={}
	user = User.objects.objects.get(phone_number=phone)
	group = UserIsGroupMember.objects.get(phone_number=user).g_id
	members = UserIsGroupMember.objects.filter(group = g_id)
	data["message"] = member.phone_number.name + " : " + message
	notification["body"] = data["message"]
	notification["title"] = "New message from " + group.name
	payload["notification"] = notification
	payload["data"] = data
	for member in members:
		if member.phone_number.phone_number != phone :
			payload["to"] = member.phone_number.reg_id
			requests.post(url,data=json.dumps(payload),headers=headers)







# data["message"] = "Do the salamander! NYEESSSSSSSSS!"
# notification["body"] = data["message"]
# notification["title"] = "New Message from EGM"
# payload ={}
# payload["notification"] = notification
# payload["data"] = data
# payload["to"]  = 'APA91bFrYlp3tEdEY7fxCgiF2G_tWqA0isrB1Bk_yfzPRIWR5h9F4_5dZnQBgCSS5nI2BT-AV5KyEMvj5Uunv2uNcyvDOhJfzoJaVKJFFVpym3yW1zyZaAJboMp4K9WnrRW6EzB0WUEWijy6cb5FQ9z3hUHAhFmXww'
# #print payload
# payload = json.dumps(payload)
# #print payload
# r = requests.post(url,data = payload,headers=headers)
# print r.content