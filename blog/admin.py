from django.contrib import admin
from .models import Category, Tag, Post  # ReadNum


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    作用:自定义分类管理工具
    admin.ModelAdmin:继承admin.ModelAdmin类
    """
    # 在后台显示id值和分类名
    list_display = ('id', 'name')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    作用:自定义标签管理工具
    admin.ModelAdmin:继承admin.ModelAdmin类
    """
    # 在后台显示od值,标签名
    list_display = ('id', 'name')


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    作用:自定义文章管理工具
    admin.ModelAdmin:继承admin.ModelAdmin类
    """
    # 在后台显示id值，博文名，创建时间，修改时间，目录，作者
    list_display = ('id', 'title', 'created_time', 'modified_time', 'category', 'author', 'get_read_num')
    # 增加过滤框,且以文章分类作过滤器
    list_filter = ['category']
    # 增加文章标题搜索字段
    search_fields = ['title']
    # 后台管理每页显示20篇文章标题
    list_per_page = 20


'''
# 测试代码
@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'post')
'''

