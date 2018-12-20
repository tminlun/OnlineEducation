#__file__ : urls.py 
__author__: '田敏伦'
__date__: '2018/12/19 0019 12:19'
from django.urls import path
from .views import OrgView, AddUserAskView, OrgDetailHome, OrgDetailCourse


app_name = "organization"
urlpatterns = [
    path('list/',OrgView.as_view(), name="org_list"),#课程机构列表
    path('add_ask/', AddUserAskView.as_view(), name="add_ask"), #我要学习
    path('org_home/<int:org_id>/', OrgDetailHome.as_view(), name="org_home"), #机构首页
    path('org_course/<int:org_id>/', OrgDetailCourse.as_view(), name="org_course"), #机构首页
]
