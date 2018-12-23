# _*_ coding:utf-8 _*_

from django.contrib import admin
from .models import ReadNum, ReadDetail
import xadmin


class ReadNumAdmin(object):
    """
    作用:自定义阅读计数管理工具
    admin.ModelAdmin:继承admin.ModelAdmin类
    """
    list_display = ['object_id', 'get_read_post', 'read_num']


xadmin.site.register(ReadNum, ReadNumAdmin)


class ReadDetailAdmin(object):
    """
    作用:自定义阅读记录管理工具
    admin.ModelAdmin:继承admin.ModelAdmin类
    """
    list_display = ['object_id', 'get_read_post', 'date', 'read_num', 'ip_address']


xadmin.site.register(ReadDetail, ReadDetailAdmin)

