# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-11-21 17:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('emailvalidator', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailregexvalidator',
            old_name='group',
            new_name='EmailDomainGroup',
        ),
    ]
