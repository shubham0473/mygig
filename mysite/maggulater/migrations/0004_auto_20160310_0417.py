# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-10 04:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('maggulater', '0003_auto_20160310_0004'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='Notes',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='test',
            name='Answer_Sheet',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='test',
            name='Questions',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='admin',
            name='Admin_Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='maggulater.MyUser'),
        ),
        migrations.AlterField(
            model_name='faculty',
            name='Faculty_Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='maggulater.MyUser'),
        ),
        migrations.AlterField(
            model_name='lecture',
            name='Date_Time',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 10, 4, 17, 19, 276399)),
        ),
        migrations.AlterField(
            model_name='notice',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2016, 3, 10, 4, 17, 19, 280434)),
        ),
        migrations.AlterField(
            model_name='student',
            name='Student_Id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='maggulater.MyUser'),
        ),
    ]