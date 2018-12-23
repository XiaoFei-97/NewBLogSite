from django.contrib import admin
from .models import ReadNum, ReadDetail


@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    """
    作用:自定义阅读计数管理工具
    admin.ModelAdmin:继承admin.ModelAdmin类
    """
    list_display = ('read_num', 'content_object')


@admin.register(ReadDetail)
class ReadNumAdmin(admin.ModelAdmin):
    """
    作用:自定义阅读记录管理工具
    admin.ModelAdmin:继承admin.ModelAdmin类
    """
    list_display = ('date', 'read_num', 'content_object')
