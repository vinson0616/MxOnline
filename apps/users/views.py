# coding:utf-8
import json

from django.shortcuts import render
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import UserProfile, EmailVerifyRecord
from operation.models import UserCourse, UserFavorite,UserMessage
from courses.models import Course
from .forms import LoginForm, RegisterForm, ForgetForm, ModifyPwdForm, UploadImageForm, UserInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from organization.models import CourseOrg, Teacher
from .models import Banner


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
                    # 重定向到首页
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {"msg": "该用户未激活!"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误!"})
        else:
            return render(request, "login.html", {"login_form": login_form})


class LoginUnSafeView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        user_name = request.POST.get("username", "")
        pass_word = request.POST.get("password", "")

        import MySQLdb
        conn = MySQLdb.connect(host='127.0.0.1',user_name='root', pass_word='rosy0616@qq.com', db='mxonline', charset='utf8')
        cursor = conn.cursor()
        sql_select = "select * from users_userprofile where email='{0}' and password='{1}'".format(user_name,pass_word)

        result = cursor.execute(sql_select)
        for row in cursor.fetchall():
            pass


# 退出登录
class LogoutView(View):
    def get(self, request):
        logout(request)
        # 重定向到首页
        return HttpResponseRedirect(reverse("index"))


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

            # 写入欢迎注册消息
            user_message = UserMessage()
            user_message.user = user_profile.id,
            user_message.message = "欢迎注册慕学在线网"
            user_message.save()

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


# 用户个人信息
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html',{

        })
    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type="application/json")


# 用户修改头像
class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        # 这种方式既有model又有form
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():  # 只有验证通过了，才会放到image_form里的clened_data这个字段里
            # image = image_form.cleaned_data['image']
            # request.user.image = image
            request.user.save()
            return HttpResponse(json.dumps({"status":"success"}),content_type='application/json')
        else:
            return HttpResponse(json.dumps({"status": "fail"}), content_type="application/json")


# 个人中心修改用户密码
class UpdatePwdView(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        pwd1 = request.POST.get("password1", "")
        pwd2 = request.POST.get("password2", "")
        if modify_form.is_valid():
            if pwd1 != pwd2:
                return HttpResponse(json.dumps({"status": "fail","msg": "密码不一致"}), content_type="application/json")
            user = request.user
            user.password = make_password(pwd1)
            user.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type="application/json")


# 发送邮箱验证码
class SendEmailCodeView(LoginRequiredMixin, View):
    def get(self, request):
        email = request.GET.get('email', '')
        if UserProfile.objects.filter(email=email):
            return HttpResponse(json.dumps({"email": "邮箱已经存在"}), content_type="application/json")

        send_register_email(email, "update_email")
        return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")


# 修改邮箱
class UpdateEmailView(LoginRequiredMixin, View):
    def post(self, request):
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')

        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code,send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse(json.dumps({"status": "success"}), content_type="application/json")
        else:
            return HttpResponse(json.dumps({"email": "验证码出错"}), content_type="application/json")


# 我的课程
class MyCourseView(LoginRequiredMixin, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return  render(request, 'usercenter-mycourse.html',{
            'user_courses': user_courses
        })


# 我的收藏 - 课程机构
class MyFavOrgView(LoginRequiredMixin,View):
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=int(org_id))
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html',{
            "org_list": org_list
        })


# 我的收藏 - 授课讲师
class MyFavTeacherView(LoginRequiredMixin,View):
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=int(teacher_id))
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html',{
            "teacher_list": teacher_list,
        })


# 我的收藏 - 课程
class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=int(course_id))
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html',{
            "course_list": course_list,
        })


# 我的消息
class MyMessageView(LoginRequiredMixin,View):
    def get(self,request):
        all_message = UserMessage.objects.filter(user=request.user.id)

        # 用户进入个人消息后清空未记录的消息
        all_unread_message = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_message in all_unread_message:
            unread_message.has_read = True
            unread_message.save()

        # 对消息进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_message, 1, request=request)
        messages = p.page(page)

        return render(request,'usercenter-message.html',{
            "messages":messages
        })


# 慕学在线网首页
class IndexView(View):
    def get(self,request):
        # 取出轮播图
        all_Banners = Banner.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request,'index.html', {
            'all_Banners': all_Banners,
            'courses':courses,
            'banner_courses':banner_courses,
            'course_orgs':course_orgs
        })


# 全局404处理函数
def page_not_found(request):
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{})
    response.status_code = 404
    return  response


# 全局500处理函数
def page_error(request):
    from django.shortcuts import render_to_response
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response