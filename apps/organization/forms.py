# coding:utf-8
__authoer__ = 'Vinson'
__date__ = '9/13/2017 05:32 PM'

import re
from django import forms

from operation.models import UserAsk


# modelForm
class UserAskForm(forms.ModelForm):

    class Meta:
        model = UserAsk
        fields = ['name', 'mobile', 'course_name']

    def clean_mobile(self):
        # 验证手机是否合法
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = "^1[13578]\d{9}$|^147\d{8}$|^176\d{8}$"
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u"手机号码非法", code="mobile_invalid")