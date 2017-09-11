# coding:utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password

from .models import UserProfile, EmailVerifyRecord
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm
from utils.email_send import send_register_email


# 需要在Setting.py加上配置，这个是自定义的auth方法
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        # 这里可以完成自己的逻辑代码
        try:
            user = UserProfile.objects.get(Q(username=username)| Q(email=username))
            if user.check_password(password):
                return  user
        except Exception as e:
            return None


# 登录
class LoginView(View):

    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, "index.html")
                else:
                    return render(request, "login.html", {"msg": "该用户未激活!"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误!"})
        else:
            return render(request, "login.html", {"login_form": login_form})


# 用户激活
class ActivateUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return  render(request,"active_fail.html")
        return render(request,"login.html")



# 注册
class RegisterView(View):

    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form":register_form})

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get("email", "")
            pass_word = request.POST.get("password", "")

            # 判断用户是否已经注册了
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"msg": "用户已经注册了","register_form": register_form})

            user_profile = UserProfile()
            user_profile.is_active = False
            user_profile.username = user_name,
            user_profile.email = user_name
            user_profile.password = make_password(pass_word)
            user_profile.save()

            send_register_email(user_name,"register")
            return render(request,"login.html")
        else:
            return render(request, "register.html", {"register_form": register_form})


# 忘记密码
class ForgetPwdView(View):
    def get(self, request):
        forget_form = ForgetForm()
        return render(request, "forgetpwd.html", {"forget_form": forget_form})

    def post(self, request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get("email", "")
            send_register_email(email, "forget")
            return render(request, "send_success.html")
        else:
            return render(request, "forgetpwd.html", {"forget_form": forget_form})


# 重置密码
class ResetView(View):
    def get(self,request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code = active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_fail.html")
        return  render(request, "login.html")


# 修改密码
class ModifyPwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        pwd1 = request.POST.get("password1", "")
        pwd2 = request.POST.get("password2", "")
        email = request.POST.get("email", "")
        if modify_form.is_valid():
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email,"msg": "密码不一致"})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd1)
            user.save()
            return render(request,"login.html")
        else:
            return render(request,"password_reset.html", {"email": email, "modify_form": modify_form})





