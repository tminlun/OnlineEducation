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


