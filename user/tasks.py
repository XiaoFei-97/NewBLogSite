from __future__ import absolute_import
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_email_by_celery(code, email, send_for_subject):
    """
    作用：使用celery异步发送邮件
    :param code: 验证码
    :param email: 邮件内容
    """
    try:
        send_mail(
            send_for_subject,
            '【蒋振飞个人博客】尊敬的用户：您正在进行"%s"操作，验证码: %s，请于30分钟内输入，网站人员不会向您索取，请勿泄露！' % (send_for_subject, code),
            'jzfblog@outlook.com',
            [email],
            fail_silently=False,
        )
    except Exception:
        # 出错尝试重新执行1次任务
        return False
    return True
