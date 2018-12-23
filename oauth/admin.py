from django.contrib import admin
from .models import OAuth_ex


@admin.register(OAuth_ex)
class OAuth_exAdmin(admin.ModelAdmin):
    list_display = ['user', 'openid']





