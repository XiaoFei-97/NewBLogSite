import xadmin
from xadmin.plugins.auth import UserAdmin as BaseAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(object):
    model = Profile
    extra = 0


class UserAdmin(BaseAdmin):
    inlines = [ProfileInline]
    list_display = ['username', 'nickname', 'email', 'is_staff', 'is_active', 'is_superuser']

    def nickname(self, obj):
        return obj.profile.nickname
    nickname.short_description = '昵称'


xadmin.site.unregister(User)
xadmin.site.register(User, UserAdmin)


class ProfileAdmin(object):
    """
    作用:自定义文章管理工具
    admin.ModelAdmin:继承admin.ModelAdmin类
    """
    list_display = ['user', 'nickname', 'image_url']


xadmin.site.register(Profile, ProfileAdmin)