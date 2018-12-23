from django import template
from blog.models import Post
from django.db.models import Q
from read_statistics.utils import get_random_recomment
import random

register = template.Library()


@register.simple_tag
def get_category_post(category):
    """
        作用：获取该目录下的所有博客
        obj：模板传递的参数，也就是category
    """
    post_list = Post.objects.filter(Q(display=0) | Q(display__isnull=True), category=category)
    return post_list[0:15]


@register.simple_tag
def get_category_count(category):
    """
        作用：计算当前分类的文章数量，并返回到模板中
        category：模板页面传入的category
    """
    return Post.objects.filter(Q(display=0) | Q(display__isnull=True), category=category).count()


@register.simple_tag
def get_date_post(year, month):
    """
        作用：获取该年月下的博客
        year：模板传递的年份
        month：模板传递的月份
    """
    post_list = Post.objects.all().filter(Q(display=0) | Q(display__isnull=True), category__status=0, created_time__year=year, created_time__month=month)
    return post_list[:15]


@register.simple_tag
def get_date_to_month(post_date):
    """
        作用：将日期格式转换成年月的形式
        obj: 对应的post_date
    """

    return str(post_date.year) +'年' + str(post_date.month) + '月'


@register.simple_tag
def get_date_count(year, month):
    """
        作用：获得该年月下的博客数量
        year: 模板传递的年份
        month：模板传递的月份
    """
    return Post.objects.filter(Q(display=0) | Q(display__isnull=True), category__status=0, created_time__year=year, created_time__month=month).count()


@register.simple_tag
def get_like_post(category, id):
    # 猜你喜欢
    # 使用Q可以过滤出不要的条件
    like_posts = set()
    posts = Post.objects.filter(~Q(id=id), category=category)

    length = posts.__len__()
    if length < 15:
        random_recommend = get_random_recomment()
        return random_recommend
    else:
        random_index = random.sample(range(length), 15)
        for i in random_index:
            like_posts.add(posts[i])

    return like_posts


@register.simple_tag
def get_post_tags(post):
    """
    获取文章下的所有标签
    :param post: 博客
    :return: 标签列表
    """
    tags_list = post.tags.all()
    return tags_list






