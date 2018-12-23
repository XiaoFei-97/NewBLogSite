from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from django.urls import reverse
from .forms import CommentForm
from django.http import JsonResponse


def update_comment(request):
    """提交评论处理功能"""
    '''
    # META获取源地址,如果获取不到源地址,就默认转到主页显示
    referer = request.META.get('HTTP_REFERER', reverse('blog:home'))
    # user = request.user
    # 数据检查,前端页面的验证不一定保险,故需在服务器端进行双重保险
    # 验证用户是否处在登录状态
    if not request.user.is_authenticated:
        context = {'message': '用户未登录',  'redirect_to': referer}
        return render(request, 'blog/error.html', context)
    # 从前端textarea标签获取用户评论内容,strip是python中的字符串处理方法,默认移除字符串头尾的空格或换行符
    text = request.POST.get('text', '').strip()
    # 验证用户输入是否为空
    if text == '':
        context = {'message': '评论内容为空',  'redirect_to': referer}
        return render(request, 'blog/error.html', context)

    try:
        content_type = request.POST.get('content_type', '')
        # 因为get到的是字符串,需要先转化为int
        object_id = int(request.POST.get('object_id', ''))

        # 找到post对象
        models_class = ContentType.objects.get(model=content_type).model_class()
        models_obj = models_class.objects.get(pk=object_id)

    except Exception as e:
        context = {'message': '评论对象不存在', 'redirect_to': referer}
        return render(request, 'blog/error.html', context)

    # 检查通过,保存数据
    comment = Comment()
    comment.user = request.user
    comment.text = text

    # Post.objects.get(pk=object_id)
    comment.content_object = models_obj
    comment.save()

    return redirect(referer)
    '''
    # META获取源地址,如果获取不到源地址,就默认转到主页显示
    # referer = request.META.get('HTTP_REFERER', reverse('blog:home'))
    # 数据检查, 前端页面的验证不一定保险, 故需在服务器端进行双重保险
    # 验证用户是否处在登录状态
    comment_form = CommentForm(request.POST, user=request.user)

    if comment_form.is_valid():
        # 检查通过,保存数据
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']

        # Post.objects.get(pk=object_id)
        comment.content_object = comment_form.cleaned_data['content_object']
        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        # 返回数据
        data = {'status': 'SUCCESS',
                'username': comment.user.get_nickname_or_username(),
                # strftime并不能正确得出当前时间,会把时区给掩盖掉,所以使用timestamp时间戳
                # 'comment_time': comment.comment_time.strftime('%Y-%m-%d %H:%M:%S'),
                'comment_time': comment.comment_time.timestamp(),
                'text': comment.text,
                'content_type': ContentType.objects.get_for_model(comment).model # 得到对应字符串
                }
        if not parent is None:
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['rook_pk'] = comment.root.pk if not comment.root is None else ''

    else:
        # context = {'message': comment_form.errors, 'redirect_to': referer}
        # return render(request, 'blog/error.html', context)
        data = {'status': 'ERROR', 'message': list(comment_form.errors.values())[0][0]}
    return JsonResponse(data)
