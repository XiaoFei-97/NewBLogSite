from django.db import models
# 跟踪安装在Django驱动项目中的所有模型，为模型提供高级通用界面。
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# auth模块是Django提供的标准权限管理系统,可以提供用户身份认证, 用户组和权限管理。
from django.contrib.auth.models import User
from django.db.models.fields import exceptions
from blog.models import Post


class Comment(models.Model):

    # 创建评论对象
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 创建评论内容,不限字数
    text = models.TextField(verbose_name=u'评论内容')
    # 时间自动创建now
    comment_time = models.DateTimeField(verbose_name=u'评论时间', auto_now_add=True)
    # 创建作者,删除且不做任何动作
    user = models.ForeignKey(User, verbose_name=u'评论人', related_name='comments',  on_delete=models.CASCADE)

    # 自关联
    root = models.ForeignKey('self', related_name='root_comment', null=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)

    def get_comment(self):
        # 此处的一个异常处理,用来捕获没有计数对象的情况
        # 例如在admin后台中,没有计数值会显示为‘-’
        try:
            post = Post.objects.get(id=self.object_id)
            return post.title
        # 对象不存在就返回0
        except exceptions.ObjectDoesNotExist:
            return 0

    get_comment.short_description = '文章'

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['comment_time']
        verbose_name = '评论'
        verbose_name_plural = '评论'

