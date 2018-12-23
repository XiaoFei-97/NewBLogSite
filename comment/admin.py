from django.contrib import admin  # admin后台管理
from .models import Comment   # 从当前应用的模型中导入Comment数据表


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    # 后台显示文章对象,评论内容,评论时间,评论者
    list_display = ('id', 'content_object', 'text', 'comment_time', 'user')
