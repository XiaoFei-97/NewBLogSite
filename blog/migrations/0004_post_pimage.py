# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2018-12-23 19:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_category_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='pimage',
            field=models.ImageField(blank=True, null=True, upload_to='upload/images/%Y/%m', verbose_name='图片上传'),
        ),
    ]
