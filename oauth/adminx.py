from .models import OAuth_ex
import xadmin


class OAuth_exAdmin(object):
    list_display = ['openid', 'user', 'oauth_type']


xadmin.site.register(OAuth_ex, OAuth_exAdmin)
