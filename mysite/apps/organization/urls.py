#__file__ : urls.py 
__author__: '田敏伦'
__date__: '2018/12/19 0019 12:19'
from django.urls import path
from .views import OrgView, AddUserAskView


app_name = "organization"
urlpatterns = [
    path('list/',OrgView.as_view(), name="org_list"),#课程机构列表（首页）
    path('add_ask/', AddUserAskView.as_view(), name="add_ask"), #我要学习
]
