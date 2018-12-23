from django import template  # 导入模板标签
from django.contrib.contenttypes.models import ContentType  # 允许从ContentType实例获取 它所代表的模型，或从该模型中检索对象
from ..models import LikeCount, LikeRecord  # 导入数据模型


register = template.Library()

# 简单模板测试
# @register.simple_tag()
# def test(a):
#     return 'this is test code:' + a


@register.simple_tag
def get_like_count(obj):
    """获取点赞数量"""
    content_type = ContentType.objects.get_for_model(obj)
    # 如果获取不到该类型对象就创建
    like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return like_count.liked_num


@register.simple_tag(takes_context=True)
def get_like_status(context, obj):
    # 获取点赞状态
    # 获取模型类或模型实例
    content_type = ContentType.objects.get_for_model(obj)
    user = context['user']
    # 如果没有登录
    if not user.is_authenticated:
        return ''
    # 如果匹配到了点赞记录(博客对象和用户)存在,就返回active,不存在就返回空
    if LikeRecord.objects.filter(content_type=content_type, object_id=obj.pk, user=user).exists():
        return 'active'
    else:
        return ''

@register.simple_tag
def get_content_type(obj):
    """获取模型实例"""
    content_type = ContentType.objects.get_for_model(obj)
    return content_type.model