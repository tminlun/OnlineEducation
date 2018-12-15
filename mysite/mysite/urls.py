"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
from django.contrib import admin
from django.urls import path,include,re_path
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView
urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),#测试，省去views渲染
    path('login/',LoginView.as_view(),name="login"),
    path('captcha/',include('captcha.urls')),#验证码
    path('register/',RegisterView.as_view(),name="register"),#注册
    #(?P)提取一个变量用作参数：<active_code>；用正则表达式取出 ActiveUserView 中所有的 active_code（任意命名要和ActiveUserView参数相同）
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name="user_active"),
    path('forget/', ForgetPwdView.as_view(), name="forget_pwd"),#忘记密码
    #找回密码链接,如果action="{% url 'reset_pwd' %}"会出错，因为这里url要有值传递给参数（active_code）
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name="reset_pwd"),
    path('modify_pwd/',ModifyPwdView.as_view(), name="modify_pwd"), #重设密码
]
