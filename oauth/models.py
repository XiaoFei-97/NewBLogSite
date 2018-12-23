from django.db import models
from django.contrib.auth.models import  User


# 用户登录的类型
oauth_type = (
    ('1', 'GitHub'),
    ('2', 'QQ'),
    ('3', 'WeiBo')
)


class OAuth_ex(models.Model):
    # User为本网站的用户模型，每个第三方账号都要绑定本站账号
    openid = models.CharField(max_length=100, default='', verbose_name='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    oauth_type = models.CharField(max_length=1, choices=oauth_type, default='1', verbose_name='来源')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = '第三方'
        verbose_name_plural = '第三方'



