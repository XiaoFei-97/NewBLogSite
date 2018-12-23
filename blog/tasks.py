from __future__ import absolute_import
from celery import shared_task
from read_statistics.utils import *


@shared_task
def get_post_list():
    """
    缓存博客列表
    """
    post_list = Post.objects.filter(Q(display=0) | Q(display__isnull=True), category__status=0)
    # 30*60表示30秒*60,也就是半小时
    cache.set('post_list', post_list, 30 * 60)


@shared_task
def get_new_publish():
    """
    缓存最新发表的15篇博客
    """
    new_publish = Post.objects.filter(Q(display=0) | Q(display__isnull=True), category__status=0)[:15]
    # 60*60表示60秒*60,也就是1小时
    cache.set('new_publish', new_publish, 30 * 60)


@shared_task
def get_new_recommend():
    """
    缓存最新推荐的博客
    """
    post_content_type = ContentType.objects.get_for_model(Post)
    new_recommend = get_new_recommend_post(post_content_type)
    # 60*60表示60秒*60,也就是1小时
    cache.set('new_recommend', new_recommend, 30 * 60)


@shared_task
def get_last_7_days_hot_data():
    """
    缓存周榜博客
    """
    last_7_days_hot_data = get_7_days_read_posts()
    # 60*60表示60秒*60,也就是1小时
    cache.set('last_7_days_hot_data', last_7_days_hot_data, 30 * 60)


@shared_task
def get_last_30_days_hot_data():
    """
    缓存月榜博客
    """
    last_30_days_hot_data = get_30_days_read_posts()
    # 60*60表示60秒*60,也就是1小时
    cache.set('last_30_days_hot_data', last_30_days_hot_data, 30 * 60)


@shared_task
def get_all_hot_posts():
    """
    缓存总榜博客
    """
    all_hot_posts = get_all_read_posts()
    # 60*60表示60秒*60,也就是1小时
    cache.set('all_hot_posts', all_hot_posts, 30 * 60)


@shared_task
def get_post_dates():
    """
    缓存日期排序的
    :return:
    """
    post_dates = Post.objects.dates('created_time', 'month', order='DESC').filter(category__status=0)
    # 60*60表示60秒*60,也就是1小时
    cache.set('post_dates', post_dates, 30 * 60)