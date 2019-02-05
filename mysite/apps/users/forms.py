from captcha.fields import CaptchaField
from django import forms
from .models import UserProfile


class LoginForm(forms.Form):
    """登录验证表单"""
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    """注册验证表单"""
    username = forms.CharField(required=True, min_length=2,max_length=10)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=6,max_length=20)
    password_again = forms.CharField(required=True, min_length=6, max_length=20)
    captcha = CaptchaField(error_messages={"invalid": "验证码输入错误"})#验证码，可以自定义错误。key（invalid是固定的），value自己可以随意写


class ForgetPwdForm(forms.Form):
    """找回密码表单"""
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码输入错误"})


class ModifyPwdForm(forms.Form):
    """找回密码表单"""
    password1 = forms.CharField(required=True, min_length=6, max_length=15)
    password2 = forms.CharField(required=True, min_length=6, max_length=15)


class ModifyImageForm(forms.ModelForm):
    """修改头像"""
    class Meta:
        model = UserProfile
        fields = ['image']


class UpdatePwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=6, max_length=15)
    password2 = forms.CharField(required=True, min_length=6, max_length=15)


class UpdateUserForm(forms.ModelForm):
    """修改个人信息"""
    class Meta:
        model = UserProfile
        fields = ['nick_name', 'brithday', 'gander', 'adress', 'mobile']
