# coding:utf-8
__authoer__ = 'Vinson'
__date__ = '9/20/2017 05:04 PM'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):  # 函数名称必须这么写，名字也一样，参数也一样
        return super(LoginRequiredMixin,self).dispatch(request, *args, **kwargs)