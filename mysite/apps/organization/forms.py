#__file__ : forms.py 
__author__: '田敏伦'
__date__: '2018/12/19 0019 11:33'

from django import forms
from operation.models import UserAsk


class UserAskForm(forms.ModelForm):
    """
    "我要咨询":使用ModelForm
    得到models的字段，input的name要和字段相等
    可以自定义forms字段
    """
    class Meta:
        model = UserAsk
        fields = ['name', 'phone_nums', 'course_name']

    # def clean_phone_nums(self):
    #     """验证手机号码是否规范"""
    #     phone_nums = self.cleaned_data['phone_nums']
    #     REGEX_PHONE_NUMS = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
    #     p = re.compile(REGEX_PHONE_NUMS)
    #     if p.match(phone_nums): #判断输入是否是一个手机号
    #         return phone_nums
    #     else:
    #         raise forms.ValidationError("手机号不规范", code="phone_nums_inval")
