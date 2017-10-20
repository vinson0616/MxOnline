# coding:utf-8
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


# 继承原来的user表，但是需要新加一些字段
class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name=u"昵称",default='')
    birthday = models.DateTimeField(verbose_name=u"生日",null=True,blank=True)
    gender = models.CharField(choices=(("male", "男"), ('female', "女")),default="female",max_length=10)
    address = models.CharField(verbose_name=u"地址", max_length=100, default=u"")
    mobile = models.CharField(max_length=11, null=True,blank=True)
    image = models.ImageField(upload_to="image/%Y%m",default=u"image/default.png",max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural= verbose_name

    # 重载unicode的方法
    def __unicode__(self):
        return self.username

    # 获取用户未读消息的数量
    def unread_nums(self):
        from operation.models import UserMessage   # 只能放在这里引用，否则会造成循环import了
        return UserMessage.objects.filter(user=self.id,has_read=False).count()


class EmailVerifyRecord(models.Model):
    code = models.CharField(max_length=20,verbose_name=u"验证码")
    email = models.EmailField(max_length=50,verbose_name=u"邮箱")
    send_type = models.CharField(choices=(('register', "注册"),('forget', "找回密码"),('update_email', u"修改邮箱")),max_length=20,verbose_name="验证码类型")
    send_time = models.DateTimeField(default=datetime.now,verbose_name="发送时间")

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code,self.email)


class Banner ( models.Model ):
    title = models.CharField(max_length=100,verbose_name=u"标题")
    image = models.ImageField(upload_to="banner/%Y%m",verbose_name=u"轮播图",max_length=100)
    url = models.URLField(max_length=200,verbose_name=u"访问地址")
    index = models.IntegerField(default=100,verbose_name=u"顺序")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u"添加时间")

    class Meta:
        verbose_name=u"轮播图"
        verbose_name_plural =verbose_name