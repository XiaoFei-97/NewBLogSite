# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-10-14 16:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0006_auto_20181014_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='oauth_ex',
            name='image_url',
        ),
        migrations.AlterField(
            model_name='oauth_ex',
            name='openid',
            field=models.CharField(default='', max_length=100, verbose_name='ID'),
        ),
    ]
