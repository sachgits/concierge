# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-05-08 12:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20180508_1058'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CroppedAvatars',
            new_name='ResizedAvatars',
        ),
    ]
