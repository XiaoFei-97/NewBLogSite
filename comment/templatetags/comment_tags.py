from django import template
from ..models import Comment
from django.contrib.contenttypes.models import ContentType
from ..forms import CommentForm

register = template.Library()

# 简单模板测试
# @register.simple_tag()
# def test(a):
#     return 'this is test code:' + a


@register.simple_tag
def get_comment_count(obj):
    """评论计数模板标签"""
    content_type = ContentType.objects.get_for_model(obj)
    return Comment.objects.filter(content_type=content_type, object_id=obj.pk).count()


@register.simple_tag
def get_comment_form(obj):
    content_type = ContentType.objects.get_for_model(obj)
    form = CommentForm(initial={
        'content_type': content_type.model,
        'object_id': obj.pk, 'reply_comment_id': 0})
    return form


@register.simple_tag
def get_comment_list(obj):
    content_type = ContentType.objects.get_for_model(obj)
    comments = Comment.objects.filter(content_type=content_type, object_id=obj.pk, parent=None)
    return comments.order_by('-comment_time')

