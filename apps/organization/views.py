# coding:utf-8

import json

from django.shortcuts import render
from django.views.generic import  View
from django.http import HttpResponse
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import CourseOrg, CityDict
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite


# 课程机构列表功能
class OrgView(View):
    def get(self, request):
        # 课程机构
        all_orgs = CourseOrg.objects.all()
        # 热门机构 取前3个的热门数据
        hot_orgs = all_orgs.order_by("-click_nums")[:3]
        # 城市
        all_citys = CityDict.objects.all()

        # 取出筛选城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 类别筛选
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 根据Sort排序包括 学习人数 和 课程数
        sort = request.GET.get("sort", "")
        if sort:
            if sort =="students":
                all_orgs = all_orgs.order_by("-students")
            elif sort == "courses":
                all_orgs = all_orgs.order_by("-course_nums")

        # 获取总的数量
        org_nums = all_orgs.count()

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 3, request=request)

        orgs = p.page(page)
        return render(request, "org-list.html",{
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort
        })


# 用户添加咨询 -- 异步操作
class AddUserAskView(View):

    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True) # 设置成True就保存到数据中了
            # 返回JSON
            return HttpResponse(json.dumps({'status': 'success', 'msg': '提交成功'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加失败'}), content_type='application/json')


# 机构首页
class OrgHomeView(View):
    def get(self,request, org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()[:3] # 有外键都能这么用
        all_teachers = course_org.teacher_set.all()[:3]
        return  render(request,'org-detail-homepage.html',{
            'all_courses': all_courses,
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


# 机构课程列表页
class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()  # 有外键都能这么用
        return render(request, 'org-detail-course.html', {
            'all_courses': all_courses,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


# 机构介绍页
class OrgDescView(View):
    def get(self, request, org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html', {
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


#  机构教师页
class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course_org.id), fav_type=2):
                has_fav = True
        all_teachers = course_org.teacher_set.all()
        return render(request, 'org-detail-teachers.html', {
            'all_teachers': all_teachers,
            'course_org': course_org,
            'current_page': current_page,
            'has_fav': has_fav
        })


# 用户收藏，用户取消收藏
class AddFavView(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        # 判断用户是否已经登录了
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}), content_type='application/json')
        # 查询是否已经被删除了
        exist_records = UserFavorite.objects.filter(user = request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果记录已经存在了，则表示用户取消收藏
            exist_records.delete()
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '收藏'}), content_type='application/json')
        else:
            user_fav =UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return HttpResponse(json.dumps({'status': 'success', 'msg': '已收藏'}), content_type='application/json')
            else:
                return HttpResponse(json.dumps({'status': 'fail', 'msg': '收藏错误'}), content_type='application/json')
