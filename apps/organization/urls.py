# coding:utf-8
__authoer__ = 'Vinson'
__date__ = '9/13/2017 05:01 PM'

from django.conf.urls import url, include

from .views import OrgView, AddUserAskView

# 关于存放课程机构的所有url
urlpatterns = [
    # 课程机构首页
    url(r'^list/$', OrgView.as_view(), name='org_list'),
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),
]