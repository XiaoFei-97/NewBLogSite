from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'like_change', views.like_change, name='like_change')
]
