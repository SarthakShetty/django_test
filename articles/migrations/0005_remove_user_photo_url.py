# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-18 14:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20160412_1546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='photo_url',
        ),
    ]
