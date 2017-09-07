# coding:utf-8
from django.shortcuts import render
from django.contrib.auth import authenticate,login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from .models import UserProfile


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
def user_login(request):
    if request.method == "POST":
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")
        user = authenticate(username = user_name,password = pass_word)
        if user is not None:
            login(request, user)
            return render(request, "index.html")
        else:
            return render(request, "login.html", {"msg": "用户名或密码错误!"})
    elif request.method == 'GET':
        return render(request,"login.html", {})