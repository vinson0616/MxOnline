# coding:utf-8
from datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField
from organization.models import CourseOrg,Teacher


class Course(models.Model):
    course_org = models.ForeignKey(CourseOrg, verbose_name=u"课程机构", null=True,blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程名")
    desc = models.CharField(max_length=500, verbose_name=u"课程描述")
    detail = UEditorField(verbose_name= u'课程详情	',width=600, height=300,  imagePath="courses/ueditor/", filePath="courses/ueditor/",default="")
    is_banner = models.BooleanField(default=False, verbose_name=u"是否轮播")
    teacher = models.ForeignKey(Teacher, verbose_name=u"讲师", null=True, blank=True)
    degree = models.CharField(choices=(("cj","初级"),("zj","中级"),("gj","高级")),max_length=2, verbose_name=u"难度")
    learn_times = models.IntegerField(default=0,verbose_name=u"学习时长(分钟数)")
    students = models.IntegerField(default=0,verbose_name=u"学习人数")
    fav_nums = models.IntegerField(default=0,verbose_name=u"收藏人数")
    image = models.ImageField(upload_to="course/%Y%m",verbose_name=u"封面图",max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name=u"点击数")
    category = models.CharField(default=u'后端开发',max_length=20, verbose_name=u"课程类别")
    tag = models.CharField(default='', verbose_name=u"课程标签", max_length=10)
    youneed_know = models.CharField(default='', max_length=300, verbose_name=u"课程描述")
    teacher_tell = models.CharField(default='', max_length=300, verbose_name=u"老师告诉你")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name =u"课程"
        verbose_name_plural = verbose_name

    # 在章节显示CourseObject，则需要重载此方法
    def __unicode__(self):
        return self.name

    # 获取课程章节数,用于界面调用
    def get_zj_nums(self):
        return self.lesson_set.all().count()
    get_zj_nums.short_description = "章节数"

    # 跳转函数
    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='http://www.baidu.com'>跳转</a>")
    go_to.short_description ="跳转"

    # 获取学习课程数
    def get_learn_users(self):
        return self.usercourse_set.all()[:5]

    # 获取课程的章节
    def get_course_lession(self):
        return self.lesson_set.all()


class BannerCourse(Course):
    class Meta:
        verbose_name =u"轮播课程"
        verbose_name_plural = verbose_name
        proxy = True  # 一定要设置成True，否则就会再生成一张新张，这样用同一张表


class Lesson(models.Model):
    course = models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100,verbose_name=u"章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"章节"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name

    # 获取章节的视频
    def get_lesson_video(self):
        return  self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u"章节")
    name = models.CharField(max_length=100, verbose_name=u"视频名")
    url = models.CharField(default="", max_length=200, verbose_name=u"访问地址")
    learn_times = models.IntegerField(default=0,verbose_name=u"学习时长(分钟数)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"视频"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course,verbose_name=u"课程")
    name = models.CharField(max_length=100,verbose_name=u"名称")
    download = models.FileField(upload_to="course/resource/%Y%m",verbose_name=u"资源文件",max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name =u"课程资源"
        verbose_name_plural = verbose_name