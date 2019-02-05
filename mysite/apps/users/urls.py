# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/1/23 0023 22:53'

from django.urls import path
from .views import UserInfoView,ModifyImageView,UpdatePwdView, SendEmailCodeView, UpdateEmailView, MyCourseView, FavCourseView, FavOrgView, FavTeacherView, MyMessageView


app_name = "users"
urlpatterns = [
    path('info/',UserInfoView.as_view(), name="user-info"),#个人中心页面显示
    path('modify_image/', ModifyImageView.as_view(), name="modify_image"),#个人中心头像
    path('update_pwd/', UpdatePwdView.as_view(), name="update_pwd"),#个人中心用户修改密码
    path('sendemail_code/', SendEmailCodeView.as_view(), name="sendemail_code"),#个人中心修改邮箱获取验证码
    path('update_email/', UpdateEmailView.as_view(), name="update_email"),  # 个人中心修改邮箱功能
    path('mycourse/', MyCourseView.as_view(), name="mycourse"),  # 我的课程
    path('fav_course/', FavCourseView.as_view(), name="fav_course"),  # 我的收藏-课程
    path('fav_org/', FavOrgView.as_view(), name="fav_org"),  # 我的收藏-机构
    path('fav_teacher/', FavTeacherView.as_view(), name="fav_teacher"),  # 我的收藏-讲师
    path('my_message/', MyMessageView.as_view(), name="my_message"),  # 我的收藏-讲师

]
