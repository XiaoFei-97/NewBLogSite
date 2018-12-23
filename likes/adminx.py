# _*_ coding:utf-8 _*_

from django.contrib import admin
from .models import LikeCount, LikeRecord
import xadmin


class LikeCountAdmin(object):
    list_display = ['object_id', 'get_like_post', 'liked_num']


class LikeRecordAdmin(object):
    list_display = ['object_id', 'get_like_post', 'user', 'liked_time']


xadmin.site.register(LikeCount, LikeCountAdmin)
xadmin.site.register(LikeRecord, LikeRecordAdmin)
