# _*_ coding:utf-8 _*_

import xadmin
from .models import Category, Tag, Post  # ReadNum
from xadmin import views


class PostAdmin(object):
    """
        作用:自定义文章管理工具
        admin.ModelAdmin:继承admin.ModelAdmin类
    """
    # 在后台显示id值，博文名，创建时间，修改时间，目录，作者
    list_display = ['id', 'title', 'created_time', 'modified_time', 'category', 'author', 'get_read_num', 'display']
    # 增加过滤框,且以文章分类作过滤器
    list_filter = ['category', 'created_time', 'author']
    # 增加文章标题搜索字段
    search_fields = ['title']
    # 后台管理每页显示20篇文章标题
    list_per_page = 20
    style_fields = {"body": "ueditor"}

    refresh_times = (60,)


xadmin.site.register(Post, PostAdmin)


class CategoryAdmin(object):
    """
        作用:自定义分类管理工具
        admin.ModelAdmin:继承admin.ModelAdmin类
    """
    # 在后台显示id值和分类名
    list_display = ['id', 'name', 'status']
    # 增加过滤框,且以文章分类作过滤器
    list_filter = ['name']
    # 增加文章标题搜索字段
    search_fields = ['name']
    # 后台管理每页显示20篇文章标题


xadmin.site.register(Category, CategoryAdmin)


class TagAdmin(object):
    """
        作用:自定义标签管理工具
        admin.ModelAdmin:继承admin.ModelAdmin类
    """
    # 在后台显示od值,标签名
    list_display = ['id', 'name']
    # 增加过滤框,且以文章分类作过滤器
    list_filter = ['name']
    # 增加文章标题搜索字段
    search_fields = ['name']
    # 后台管理每页显示20篇文章标题


xadmin.site.register(Tag, TagAdmin)


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True  # 调用更多主题


class GlobalSetting(object):
    # 设置网站标题
    site_title = "后台管理系统"
    # 设置网站页脚
    site_footer = "蒋振飞的博客"
    # 设置应用图标
    # menu_style = "accordion"


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)
