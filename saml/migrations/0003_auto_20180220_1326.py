# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-02-20 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('saml', '0002_auto_20180220_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='identityprovider',
            name='sloId',
            field=models.URLField(max_length=256, null=True),
        ),
    ]
