# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-12-08 09:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likecount',
            name='object_id',
            field=models.PositiveIntegerField(verbose_name='ID'),
        ),
    ]
