# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-04-13 07:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20180404_1014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='new_email',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
    ]
