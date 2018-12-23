from django.conf.urls import include, url
from oauth import views as oauth_views

urlpatterns = [
    # 其他的就省略不显示

    url(r'github_login', oauth_views.github_login, name='github_login'),
    url(r'github_check', oauth_views.github_check, name='github_check'),
    url(r'qq_login', oauth_views.qq_login, name='qq_login'),
    url(r'qq_check', oauth_views.qq_check, name='qq_check'),
    url(r'weibo_login', oauth_views.weibo_login, name='weibo_login'),
    url(r'weibo_check', oauth_views.weibo_check, name='weibo_check'),
    url(r'email', oauth_views.bind_email, name='bind_email'),   # 通过邮箱将第三方账户绑定到本站账号

]