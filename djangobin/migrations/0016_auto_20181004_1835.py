# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-10-04 15:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('djangobin', '0015_auto_20181002_0343'),
    ]

    operations = [
        migrations.AddField(
            model_name='snippet',
            name='Cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='snippet',
            name='Comment',
            field=models.TextField(blank=True),
        ),
    ]