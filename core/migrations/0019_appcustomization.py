# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-05 19:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20180118_1441'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppCustomization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_title', models.CharField(max_length=50)),
                ('color_hex', models.CharField(max_length=6, verbose_name="your product's main brand color (Hex)")),
                ('logo_image', models.ImageField(blank=True, null=True, upload_to='')),
                ('app_favicon', models.ImageField(blank=True, null=True, upload_to='')),
                ('app_background_photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('app_background_options', models.CharField(choices=[('C', 'Cover'), ('T', 'Tiled')], max_length=1)),
                ('display_language_toggle', models.BooleanField(default=True)),
                ('display_logo_title', models.BooleanField(default=True, verbose_name='Display Logo and Title together')),
            ],
        ),
    ]
