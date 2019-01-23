# _*_ encoding:utf-8 _*_
__author__: '田敏伦'
__date__: '2019/1/23 0023 22:53'

from django.urls import path
from .views import UserInfoView,ModifyImageView


app_name = "users"
urlpatterns = [
    path('info/',UserInfoView.as_view(), name="user-info"),#用户信息页面显示
    path('modify_image/', ModifyImageView.as_view(), name="modify_image"),#头像
]
