"""blogproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from blog.search_indexes import MySeachView
import xadmin


urlpatterns = [
    url(r'^task/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    # 通过在根目录下的url加上namespace属性可以实现反向解析的功能
    # 注意:在根目录的url为namespace而项目的url是name
    url(r'^', include('blog.urls', namespace='blog')),    # 该地址就在ip根目录下
    url(r'^', include('comment.urls', namespace='comment')),
    url(r'^', include('likes.urls', namespace='likes')),
    url(r'^', include('user.urls', namespace='user')),
    url(r'^search/', MySeachView(), name='haystack_search'),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^oauth/', include('oauth.urls', namespace='oauth')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
