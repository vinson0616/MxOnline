# coding:utf-8
__authoer__ = 'Vinson'
__date__ = '9/7/2017 03:26 PM'
from django import forms
from captcha.fields import CaptchaField


# 专门用来验证form表单的
class LoginForm(forms.Form):
    username = forms.CharField(required=True)  # 页面上的name名称必须保持一致
    password = forms.CharField(required=True, min_length=5)


# 注册验证
class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid":"验证码错误"})