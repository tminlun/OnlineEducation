# _*_ encoding:utf-8 _*_  使用注释必须加这个
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
from django.conf import settings #上传图片
from django.conf.urls.static import static #上传图片
from django.views.static import serve
from django.conf.urls import url
from users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, LogoutView, IndexView
from organization.views import OrgView


urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('', IndexView.as_view(), name='index'),#首页（TemplateView.as_view(template_name='index.html')测试，省去views渲染）
    path('login/',LoginView.as_view(),name="login"),#登录
    path('captcha/',include('captcha.urls')),#验证码
    path('register/',RegisterView.as_view(),name="register"),#注册
    #(?P)提取一个变量用作参数：<active_code>；用正则表达式取出 ActiveUserView 中所有的 active_code（任意命名要和ActiveUserView参数相同）
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name="user_active"),
    path('forget/', ForgetPwdView.as_view(), name="forget_pwd"),#忘记密码
    #找回密码链接,如果action="{% url 'reset_pwd' %}"会出错，因为这里url要有值传递给参数（active_code）
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name="reset_pwd"),
    path('modify_pwd/',ModifyPwdView.as_view(), name="modify_pwd"), #重设密码
    path("org/", include('organization.urls',namespace="org")), #课程机构:前缀名（namespace="org" 防止冲突）
    path('logout/',LogoutView.as_view(), name="logout"),#注销
    path('course/',include("course.urls", namespace="course")), #公开课
    path('users/',include("users.urls", namespace="users")), #用户信息

    #404，手动配置static路径
    # url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    #富文本编辑器
    path('ueditor/',include('DjangoUeditor.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler404 = users.views.path_not_found #全局404页面配置
# handler500 = "users.views.page_error" #全局500页面配置
