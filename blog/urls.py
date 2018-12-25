# _*_ coding:utf-8 _*_

from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home, name='home'),  # 访问地址:主机名+端口号/
    url(r'^detail/(?P<pk>\d+)$', views.detail, name='detail'),  # 访问地址:主机名+端口号/detail/pk
    url(r'^category/(?P<pk>\d+)$', views.category, name='category'),  # 访问地址:主机名+端口号/category/pk
    url(r'^blog', views.blog, name='blog'),  # 访问地址:主机名+端口号/blog
    url(r'^ajax_blog', views.ajax_blog, name='ajax_blog'),  # 访问地址:主机名+端口号/blog
    url(r'^date/(\d+)/(\d+)', views.date, name='date'),  # 访问地址:主机名+端口号/date/年/月
    url(r'^findWords', views.findWords, name='findWords'),
    url(r'^looking', views.looking, name='looking')
]

handler404 = views.page_not_found
