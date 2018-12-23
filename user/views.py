from django.shortcuts import redirect, render
# from comment.models import Comment   # 导入Comment评论模块
# contenttypes 是Django内置的一个应用，可以追踪项目中所有app和model的对应关系，并记录在ContentType表中
from django.contrib import auth  # auth模块是Django提供的标准权限管理系统,可以提供用户身份认证, 用户组和权限管理。
from django.urls import reverse    # 反向解析
from django.contrib.auth.models import User
# from comment.models import Comment
# from comment.forms import CommentForm
from .forms import *
from django.http import JsonResponse
from .models import Profile
# from django.core.mail import send_mail
from .tasks import *
import string
import random
import time


def login_for_modal(request):
    """
    模态框
    :param request: 请求对象
    :return: json数据
    """
    login_form = LoginModalForm(request.POST)
    if login_form.is_valid():
        # cleaned_data是一个字典,包含了字段的信息
        # 表示清理过或者整理过的数据,比较干净的数据
        # username = login_form.cleaned_data['username']
        # password = login_form.cleaned_data['password']
        # user = auth.authenticate(username=username, password=password)
        # 判断用户是否存在
        # if user is not None:
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        # 如果没有获取到源页面就返回到首页
        data = {'status': 'SUCCESS'}
    else:
        data = {'status': 'ERROR'}
    return JsonResponse(data)


def register_for_modal(request):
    """
    用户注册功能相关处理
    :param request: 请求对象
    :return: 注册成功返回首页，失败返回注册表单
    """
    reg_form = RegModalForm(request.POST, request=request)
    # 判断是否有效
    # 验证通过
    if reg_form.is_valid():
        # 第一种注册方法
        username = reg_form.cleaned_data['username']
        email = reg_form.cleaned_data['email']
        password = reg_form.cleaned_data['password']
        verification_code = reg_form.cleaned_data['verification_code'].lower()
        # 增加ajax的判断
        if User.objects.filter(username=username).exists():
            data = {'status': '100'}
            return JsonResponse(data)
        if User.objects.filter(email=email).exists():
            data = {'status': '200'}
            return JsonResponse(data)
        code = request.session.get('register_code', '').lower()
        if not (code != '' and code == verification_code):
            data = {'status': '300'}
            return JsonResponse(data)
        # 创建用户
        user = User.objects.create_user(username, email, password)
        user.save()
        # 登录用户
        user = auth.authenticate(username=username, password=password)
        auth.login(request, user)
        # 清除session
        del request.session['register_code']
        # return redirect(request.GET.get('from', reverse('blog:home')))
        data = {'status': 'SUCCESS'}
    # 验证失败
    else:
        data = {'status': 'ERROR'}
    return JsonResponse(data)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('blog:home')))


def profile(request):
    context = {}
    return render(request, 'user/profile.html', context)


def about(request):
    context = {'LoginModalForm': LoginModalForm(),
               "RegModalForm": RegModalForm(),
               'ForgotPasswordModalForm': ForgotPasswordModalForm(),
               }
    return render(request, 'user/about.html',   context)


def chname(request):
    """修改昵称"""
    if request.method == 'POST':
        name_form = ChangeNameForm(request.POST, user=request.user)
        if name_form.is_valid():
            # 获取上次访问地址
            referer = request.POST.get("referer")

            new_nickname = name_form.cleaned_data['new_nickname']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = new_nickname
            profile.save()
            # return redirect(request.GET.get('from', reverse('blog:home')))
            return redirect(referer)

    else:
        name_form = ChangeNameForm()

    referer = request.META.get('HTTP_REFERER', '/')
    context = {'name_form': name_form,
               'referer': referer,
               }
    return render(request, 'user/chname.html', context)


def chpwd(request):
    """修改密码"""
    if request.method == 'POST':
        password_form = ChangePasswordForm(request.POST, user=request.user)
        if password_form.is_valid():
            user = request.user
            new_password = password_form.cleaned_data['new_password']
            # past_password = password_form.cleaned_data['past_password']

            # 直接赋值是没办法加密的
            user.set_password(new_password)
            user.save()
            auth.login(request, user)
            return redirect('blog:blog')

    else:
        password_form = ChangePasswordForm()

    context = {'password_form': password_form}
    return render(request, 'user/chpwd.html', context)


def forgot_password_modal(request):
    """忘记密码"""
    forgot_form = ForgotPasswordModalForm(request.POST, request=request)
    if forgot_form.is_valid():
        new_password = forgot_form.cleaned_data['new_password']
        email = forgot_form.cleaned_data['password_email']
        verification_code = forgot_form.cleaned_data['password_verification_code'].lower()
        # 增加ajax判断
        if not User.objects.filter(email=email).exists():
            data = {'status': '100'}
            return JsonResponse(data)
        code = request.session.get('forgot_password_code', '').lower()
        if not (code != '' and code == verification_code):
            data = {'status': '200'}
            return JsonResponse(data)
        user = User.objects.get(email=email)
        user.set_password(new_password)
        user.save()

        # 情书session
        del request.session['forgot_password_code']
        data = {'status': 'SUCCESS'}
    else:
        data = {'status': 'ERROR'}
    return JsonResponse(data)


def bind_email(request):
    """绑定邮箱"""
    if request.method == 'POST':
        email_form = BindEmailForm(request.POST, request=request)
        if email_form.is_valid():
            # 获取上次访问地址
            referer = request.POST.get("referer")
            email = email_form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清除session
            del request.session['bind_eamil_code']
            # return redirect(request.GET.get('from', reverse('blog:home')))
            return redirect(referer)

    else:
        email_form = BindEmailForm()
    referer = request.META.get('HTTP_REFERER', '/')
    context = {'email_form': email_form,
               'referer': referer,
               }
    return render(request, 'user/bind_email.html', context)


def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}
    if email != '':
        # 生成验证码
        # 利用random的sample方法
        # 参数：string.ascii_letters，返回所有大小写字母
        # 参数：string.digits,返回0-9的数字
        # 返回的结果是一个列表
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 60:
            data["status"] = 'ERROR'
        else:
            # session默认有效期是两星期
            request.session[send_for] = code
            request.session['send_code_time'] = now

            # 发送邮件
            # send_mail(
            #     '绑定邮箱',
            #     '验证码: %s' % code,
            #     'XiaoFei-97@outlook.com',
            #     [email],
            #     fail_silently=False,
            # )
            send_for_subject = '邮件发送'
            if send_for == 'register_code':
                send_for_subject = '账号注册'
            if send_for == 'bind_eamil_code':
                send_for_subject = '邮箱绑定'
            if send_for == 'forgot_password_code':
                send_for_subject = '找回密码'
            flag = send_email_by_celery(code, email, send_for_subject)
            if flag:
                data["status"] = 'SUCCESS'
            else:
                data["status"] = '100'
    else:
        data["status"] = 'ERROR'
    return JsonResponse(data)
