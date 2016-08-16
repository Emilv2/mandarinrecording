# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-07 22:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('N', 'No_answer')], max_length=2)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('registration_date', models.DateTimeField()),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
    ]
