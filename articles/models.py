'''
user(phone_number(pkey),age,name,photo_url,date_creation)
group(g_id(pkey),name,date_creation, destination)
group_message(gm_id(pkey),video_url,photo_url,text)
user_is_admin_group(g_id(pkey)(fkey from group),phone_number(fkey from user))
user_is_group_member(g_id(pkey)(fkey from group),phone_number(pkey)(fkey from user))
user_send_group_message(phone_number(pkey)(fkey from user),gm_id(pkey)(fkey from group_message),g_id(fkey from group))
user_receives_group_message(phone_number(pkey)(fkey from user),gm_id(pkey)(fkey from group_message),g_id(fkey from group))
'''

from __future__ import unicode_literals

from django.db import models

# Create your models here.

class group(models.Model):
	g_id = models.CharField(max_length=25)
	name = models.CharField(max_length=25)
	date_creation = models.DateTimeField('date published')
	destination = models.CharField(max_length=50)

class group_message(models.Model):
	gm_id = models.CharField(max_length=25)
	video_url = models.URLField(max_length=100)
	photo_url = models.URLField(max_length=100)
	text = models.CharField(max_length=500)

class user_is_admin_group:
	g_id = models.ForeignKey('group', on_delete=models.CASCADE)
	phone_number = models.ForeignKey('user', on_delete=models.CASCADE)
	
class user_is_group_member:
	g_id = models.ForeignKey('group', on_delete=models.CASCADE)
	phone_number = models.ForeignKey('user', on_delete=models.CASCADE)
	
	
