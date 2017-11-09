# coding:utf-8
__authoer__ = 'Vinson'
__date__ = '9/6/2017 04:48 PM'

import xadmin
from .models import Course, Lesson, Video, CourseResource,BannerCourse
from organization.models import CourseOrg


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'get_zj_nums', 'go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    ordering = ['-click_nums']  # 默认进入按照点击数倒序排列
    readonly_fields = ['click_nums']  # 设置某些字段为只读，则用户不能编辑
    list_editable = ['degree', 'desc'] # 可以直接在列表页进行编辑，非常好用
    exclude = ['fav_nums']   # 设置隐藏某个字段，这个字段和readonly_fields是冲突的，如果readonly已经有这个字段了，则exclude设置就会无效
    inlines = [LessonInline,CourseResourceInline]  # 只能嵌套一次，不能嵌套两次，比如视频就不能inline
    refresh_times = [3,5]  # 自动刷新页面，每隔一段时间
    style_fields = {"detail": "ueditor"}
    import_excel = True

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    # 在保存课程的时候，统计课程机构的课程数
    def save_models(self):
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request,*args,**kwargs):
        if 'excel' in request.FILES:
            pass
        return  super(CourseAdmin,self).post(request,args,kwargs)

class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    ordering = ['-click_nums']  # 默认进入按照点击数倒序排列
    readonly_fields = ['click_nums']  # 设置某些字段为只读，则用户不能编辑
    exclude = ['fav_nums']   # 设置隐藏某个字段，这个字段和readonly_fields是冲突的，如果readonly已经有这个字段了，则exclude设置就会无效
    inlines = [LessonInline,CourseResourceInline]  # 只能嵌套一次，不能嵌套两次，比如视频就不能inline

    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time'] # course__name表示外键的名称


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course', 'name', 'download', 'add_time']

xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)