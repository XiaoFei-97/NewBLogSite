# _*_ coding:utf-8 _*_

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^comment/update_comment$', views.update_comment, name='update_comment')
]
