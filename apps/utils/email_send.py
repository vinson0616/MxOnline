# coding:utf-8
__authoer__ = 'Vinson'
__date__ = '9/8/2017 02:47 PM'

from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


def send_register_email(email, send_type="register"):
    email_record = EmailVerifyRecord()
    code = generate_random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type =send_type
    email_record.save()

    # 发送邮件
    email_title = ""
    email_body = ""

    if send_type == "register":
        email_title = "慕学在线网注册激活链接"
        email_body = "请点击下面的链接激活你的账号： http://127.0.0.1:8000/activate/{0}".format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status :
            pass


# 生成随机字符串
def generate_random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz01234567890'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0, length)]
    return str
