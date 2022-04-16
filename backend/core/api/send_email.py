# _*_ coding: utf-8 _*_
"""send email function
"""
# import datetime
import random
import string
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
from core.models.user import ConfirmString, User


def make_confirm_string(email: str):
    """generate confirm string

    Arguments:
        user {User} -- user

    Returns:
        str -- confirm string
    """
    # now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    code = "".join(random.sample(string.ascii_letters + string.digits, 4))
    if ConfirmString.objects.filter(email=email).exists():
        confirm = ConfirmString.objects.get(email=email)
        confirm.code = code
        confirm.save()
    else:
        ConfirmString.objects.create(code=code, email=email)
    return code


def send_email(email, code):
    """send register email

    Arguments:
        email {str} -- email addr
        code {str} -- check code
    """
    subject = '来自Paper Daily的注册邮件'

    text_content = '感谢注册Paper Daily，你的邮箱验证码是:' + str(code)

 
    send_mail(subject, text_content, settings.EMAIL_HOST_USER,[email], fail_silently=False)



def send_forget(email, code):
    """send register email

    Arguments:
        email {str} -- email addr
        code {str} -- check code
    """

    subject = '来自Paper Daily的修改密码确认邮件'

    text_content = '感谢使用Paper Daily，你的邮箱验证码是:' + str(code)

 
    send_mail(subject, text_content, settings.EMAIL_HOST_USER,[email], fail_silently=False)
