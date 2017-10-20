# coding:utf-8
import json

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import Course, CourseResource,Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin  # Mixin结尾的都是基础函数


# 课程列表首页
class CourseListView(View):
    def get(self,request):
        all_courses = Course.objects.all().order_by("-add_time")

        hot_courses = Course.objects.all().order_by("-click_nums")[:3]

        # 搜索公开课
        search_keywords = request.GET.get('keywords','')
        if search_keywords:
            all_courses = all_courses.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(detail__icontains=search_keywords))  # 有关于i的是不区分大小写的

        # 课程排序： 根据Sort排序包括 最热门 和 参与人数
        sort = request.GET.get("sort", "")
        if sort:
            if sort == "students":
                all_courses = all_courses.order_by("-students")
            elif sort == "hot":
                all_courses = all_courses.order_by("-click_nums")

        # 对课程进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 6, request=request)

        courses = p.page(page)
        return render(request, 'course-list.html', {
            'all_courses': courses,
            'hot_courses': hot_courses,
            'sort': sort
        })


# 课程详细页面首页
class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加课程点击数
        course.click_nums += 1
        course.save()

        has_course_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.id),fav_type=1 ):
                has_course_fav = True
        has_org_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=int(course.course_org.id),fav_type=2):
                has_org_fav = True

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag).exclude(id=course_id)[:1]
        else:
            relate_courses = []

        return  render(request, 'course-detail.html', {
            'course': course,
            'relate_courses': relate_courses,
            'has_course_fav': has_course_fav,
            'has_org_fav': has_org_fav
        })


# 课程章节信息
class CourseInfoView(LoginRequiredMixin, View):
    def get(self,request, course_id):
        course = Course.objects.get(id = int(course_id))

        # 学习人数+1
        course.students +=1
        course.save()

        # 查询用户是否已经关联了该课程
        user_query_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_query_courses:
            user_query_course = UserCourse(user=request.user, course=course)
            user_query_course.save()

        # 该课的学生还学过的所有课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.id for user_course in user_courses]
        # 获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return  render(request, 'course-video.html',{
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses
        })


# 课程评论   继承了Login，如果用户未登录，则必须得先登录
class CommentsView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        # 该课的学生还学过的所有课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.id for user_course in user_courses]
        # 获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.all()
        return  render(request,'course-comment.html',{
            "course": course,
            "all_resources": all_resources,
            "all_comments": all_comments,
            "relate_courses": relate_courses
        })


# 用户添加课程评论
class AddCommentsView(View):
    def post(self,request):
        # 判断用户是否已经登录了
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '用户未登录'}), content_type='application/json')

        course_id = request.POST.get("course_id",0)
        comments = request.POST.get("comments", "")
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.course = course
            course_comments.comments = comments
            course_comments.user = request.user
            course_comments.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': '添加成功'}), content_type='application/json')
        else:
            return HttpResponse(json.dumps({'status': 'fail', 'msg': '添加失败'}), content_type='application/json')


# 视频播放页面
class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        # 查询用户是否已经关联了该课程
        user_query_courses = UserCourse.objects.filter(user=request.user, course=course)
        if not user_query_courses:
            user_query_course = UserCourse(user=request.user, course=course)
            user_query_course.save()

        # 该课的学生还学过的所有课程
        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        course_ids = [user_course.id for user_course in user_courses]
        # 获取学过该用户学过其他的所有课程
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        all_resources = CourseResource.objects.filter(course=course)
        return render(request, 'course-play.html', {
            "course": course,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
            "video": video
        })