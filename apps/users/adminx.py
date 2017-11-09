# coding:utf-8
__authoer__ = 'Vinson'
__date__ = '9/6/2017 04:39 PM'

import xadmin
from  xadmin import views
from xadmin.plugins.auth import UserAdmin

from .models import EmailVerifyRecord
from .models import Banner



# 这个是全局设置
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    site_title = "慕学后台管理系统"
    site_footer = "慕学在线网"
   #  menu_style ="accordion"


class EmailVerifyRecordAdmin(object):
    list_display =['code', 'email', 'send_type', 'send_time']
    search_fields=['code', 'email', 'send_type']  # 查询条件
    list_filter = ['code', 'email', 'send_type', 'send_time']  # 过滤器 - 高级搜索
    model_icon = 'fa fa-envelope-o'



class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']

xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner, BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)