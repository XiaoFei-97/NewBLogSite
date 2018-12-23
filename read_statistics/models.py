from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models.fields import exceptions
from django.contrib.auth.models import User
# from blog.models import Post


class ReadNum(models.Model):
    """
    作用：单篇博客计数的模型类
    models.Model继承model.Model模型类
    """
    read_num = models.IntegerField(default=0, verbose_name=u'阅读次数')

    content_type = models.ForeignKey(ContentType, verbose_name=u'类型', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name=u'ID')

    # 使用contenttypes模型类来找出关联blog
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = '阅读计数'
        verbose_name_plural = '阅读计数'
        ordering = ['-read_num']


class ReadNumExpandMethod(object):
    """
    作用：计数扩展类,此方法放在admin的list_display中
    object：继承object模型类
    """
    def get_read_num(self):
        ct = ContentType.objects.get_for_model(self)
        # 此处的一个异常处理,用来捕获没有计数对象的情况
        # 例如在admin后台中,没有计数值会显示为‘-’
        try:
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        # 对象不存在就返回0
        except exceptions.ObjectDoesNotExist:
            return 0
    get_read_num.short_description = '阅读'


class ReadDetail(models.Model):
    """
    作用：根据日期计数的模型类
    models.Model继承model.Model模型类
    """
    read_num = models.IntegerField(default=0, verbose_name=u'阅读次数')
    date = models.DateField(default=timezone.now, verbose_name=u'阅读日期',)

    content_type = models.ForeignKey(ContentType, verbose_name=u'类型', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(verbose_name=u'ID')
    content_object = GenericForeignKey('content_type', 'object_id')

    # 记录IP地址
    ip_address = models.CharField(max_length=15, verbose_name="来源", blank=True, null=True)

    # 记录User，这里可能没有登录用户，所以要允许为空
    # user = models.ForeignKey(User, verbose_name="浏览者", blank=True, null=True)

    class Meta:
        verbose_name = '阅读记录'
        verbose_name_plural = '阅读记录'
        ordering = ['-date']

