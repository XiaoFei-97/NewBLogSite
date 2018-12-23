from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from blog.models import Post
from django.db.models.fields import exceptions


class LikeCount(models.Model):
    """点赞的模型类"""
    # 点赞的对象
    content_type = models.ForeignKey(ContentType, verbose_name=u'类型', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name=u'ID')
    content_object = GenericForeignKey('content_type', 'object_id')
    # 点赞数
    liked_num = models.IntegerField(verbose_name=u'点赞数', default=0)

    def get_like_post(self):
        # 此处的一个异常处理,用来捕获没有计数对象的情况
        # 例如在admin后台中,没有计数值会显示为‘-’
        try:
            post = Post.objects.get(id=self.object_id)
            return post.title
        # 对象不存在就返回0
        except exceptions.ObjectDoesNotExist:
            return 0

    get_like_post.short_description = '文章'

    class Meta:
        verbose_name = '点赞计数'
        verbose_name_plural = '点赞计数'
        ordering = ['-liked_num']


class LikeRecord(models.Model):
    # 点赞记录的模型类
    # 被点赞的信息
    content_type = models.ForeignKey(ContentType, verbose_name=u'类型', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name=u'点赞ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, verbose_name=u'点赞人', on_delete=models.CASCADE)
    liked_time = models.DateTimeField(auto_now_add=True, verbose_name=u'点赞时间')

    def get_like_post(self):
        # 此处的一个异常处理,用来捕获没有计数对象的情况
        # 例如在admin后台中,没有计数值会显示为‘-’
        try:
            post = Post.objects.get(id=self.object_id)
            return post.title
        # 对象不存在就返回0
        except exceptions.ObjectDoesNotExist:
            return 0

    get_like_post.short_description = '文章'

    class Meta:
        verbose_name = '点赞记录'
        verbose_name_plural = '点赞记录'
        ordering = ['-liked_time']


