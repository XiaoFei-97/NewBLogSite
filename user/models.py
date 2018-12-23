from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户名')
    nickname = models.CharField(max_length=20, verbose_name='昵称')
    image_url = models.URLField(default='', verbose_name='头像地址')

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = '昵称'
        verbose_name_plural = '昵称'


def get_nickname(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.nickname
    else:
        return ''


def get_nickname_or_username(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        if profile.nickname:
            return profile.nickname
        return self.username
    else:
        return self.username


def has_nickname(self):
    return Profile.objects.filter(user=self).exists()


def get_image_url(self):
    if Profile.objects.filter(user=self).exists():
        profile = Profile.objects.get(user=self)
        return profile.image_url
    else:
        return ''


User.get_nickname = get_nickname
User.get_nickname_or_username = get_nickname_or_username
User.has_nickname = has_nickname
User.get_image_url = get_image_url


