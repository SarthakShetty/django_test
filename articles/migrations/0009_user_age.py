# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-25 09:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_auto_20160424_0849'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=20),
            preserve_default=False,
        ),
    ]
