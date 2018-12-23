from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user/register_for_modal/', views.register_for_modal, name='register_for_modal'),  # 访问地址:主机名+端口号/register
    url(r'^login_for_modal/', views.login_for_modal, name='login_for_modal'),
    url(r'^user/logout/', views.logout, name='logout'),
    url(r'^user/profile/', views.profile, name='profile'),
    url(r'^about/', views.about, name='about'),
    url(r'^user/chname/', views.chname, name='chname'),
    url(r'^user/chpwd/', views.chpwd, name='chpwd'),
    url(r'^user/forgotpwd/', views.forgot_password_modal, name='forgot_password_modal'),
    url(r'^user/email/', views.bind_email, name='bind_email'),
    url(r'^send_verification_code/', views.send_verification_code, name='send_verification_code'),
]