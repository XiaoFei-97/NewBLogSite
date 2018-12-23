# _*_ coding:utf-8 _*_

from django.db import models
from django.contrib.auth.models import User  # 引入USER
from django.contrib.contenttypes.fields import GenericRelation
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail, ReadNum
from DjangoUeditor.models import UEditorField
from django.contrib.contenttypes.models import ContentType
from django.db.models.fields import exceptions


class Category(models.Model):
    """
    Django 要求模型必须继承 models.Model 类。
    Category 只需要一个简单的分类名 name 就可以了。
    CharField 指定了分类名 name 的数据类型，CharField 是字符型，
    CharField 的 max_length 参数指定其最大长度，超过这个长度的分类名就不能被存入数据库。
    """
    CATEGORY_DISPALY = (
        (0, u'展示'),
        (1, u'隐藏'),
    )

    name = models.CharField(max_length=20, verbose_name=u'分类')
    status = models.IntegerField(choices=CATEGORY_DISPALY, default=0, verbose_name='是否发表', null=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'

    def __str__(self):

        return self.name


class Tag(models.Model):
    """
    标签 Tag 也比较简单，和 Category 一样。
    再次强调一定要继承 models.Model 类！
    """
    name = models.CharField(max_length=100, verbose_name=u'标签')

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'

    def __str__(self):

        return self.name


class Post(models.Model, ReadNumExpandMethod):
    """
    文章的数据库表稍微复杂一点，主要是涉及的字段更多。
    """
    Post_Display = (
        (0, u'直接发表'),
        (1, u'保留草稿'),
    )
    # 文章标题
    # u'文章标题'可以在后台显示里面的字段名
    title = models.CharField(max_length=70, verbose_name=u'文章标题',)

    # 文章正文，我们使用了 TextField。
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    body = UEditorField(verbose_name=u'内容', width=580, height=340, toolbars="full",
                        imagePath="images/", filePath="files/",
                        upload_settings={"imageMaxSize": 1204000, "imagePathFormat": "images/%(basename)s_%(datetime)s.%(extname)s"},
                        )

    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    # auto_now_add=True时间可以被确定为现在的时间,不需要在后台对该字段名进行操作
    created_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    modified_time = models.DateTimeField(verbose_name=u'修改时间', auto_now_add=True)

    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(verbose_name=u'摘要', max_length=200, blank=True)

    # 这是分类与标签，分类与标签的模型已经定义在上面。
    # 这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以使用的是 ForeignKey，即一对多的关联关系。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以使用 ManyToManyField，表明这是多对多的关联关系。
    # 文章可以没有标签，因此为标签 tags 指定了 blank=True。

    category = models.ForeignKey(Category, verbose_name=u'分类')
    tags = models.ManyToManyField(Tag, blank=True, verbose_name=u'标签', related_name='tag_post')

    read_detail = GenericRelation(ReadDetail)

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django已经写好的用户模型。
    # 通过 ForeignKey 把文章和 User 关联了起来。
    # 规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    # on_delete=models.ON_DOTHING表示删除关联数据,什么也不做
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=u'作者')

    display = models.IntegerField(choices=Post_Display, verbose_name='是否发表', null=True)

    pimage = models.ImageField(upload_to='upload/images/%Y/%m', max_length=100, verbose_name=u'图片上传', null=True, blank=True)
    # read_num = models.IntegerField(default=0)

    '''
    def get_read_num(self):
        try:
            return self.readnum.read_num

        except exceptions.ObjectDoesNotExist:
            return 0
    '''
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_time']


def get_read_post(self):
    # 此处的一个异常处理,用来捕获没有计数对象的情况
    # 例如在admin后台中,没有计数值会显示为‘-’
    try:
        post = Post.objects.get(id=self.object_id)
        return post.title
    # 对象不存在就返回0
    except exceptions.ObjectDoesNotExist:
        return 0


get_read_post.short_description = '文章'

ReadDetail.get_read_post = get_read_post
ReadNum.get_read_post = get_read_post



'''
class ReadNum(models.Model):
    read_num = models.IntegerField(u'阅读次数', default=0)
    post = models.OneToOneField(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.read_num

    class Meta:
        verbose_name = '阅读'
        verbose_name_plural = '阅读'
'''