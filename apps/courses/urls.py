# coding:utf-8
__authoer__ = 'Vinson'
__date__ = '9/18/2017 02:36 PM'

from django.conf.urls import url, include
from .views import CourseListView, CourseDetailView, CourseInfoView, CommentsView, AddCommentsView

# 关于存放课程机构的所有url
urlpatterns = [
    # 课程首页
    url(r'^list/$', CourseListView.as_view(), name='course_list'),
    # 课程详细页面
    url(r'^detail/(?P<course_id>\d+)/$',CourseDetailView.as_view(),name='course_detail'),
    # 课程视频详细信息
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),
    # 课程评论
    url(r'^comments/(?P<course_id>\d+)/$', CommentsView.as_view(), name='course_comments'),
    # 添加课程评论
    url(r'^add_comments/$', AddCommentsView.as_view(), name='add_comments'),
]