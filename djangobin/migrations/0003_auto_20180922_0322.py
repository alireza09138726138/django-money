# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-09-21 23:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('djangobin', '0002_snippet_ti'),
    ]

    operations = [
        migrations.RenameField(
            model_name='snippet',
            old_name='ti',
            new_name='t',
        ),
    ]