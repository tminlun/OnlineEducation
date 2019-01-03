#__file__ : urls.py 
__author__: '田敏伦'
__date__: '2018/12/19 0019 12:19'
from django.urls import path
from .views import OrgView, AddUserAskView, OrgDetailHome, TeacherDetailView, OrgDetailCourse, OrgDescCourse, OrgTeachersCourse,AddFavView,TeacherListView


app_name = "organization"
urlpatterns = [
    path('org_list/',OrgView.as_view(), name="org_list"),#课程机构列表
    path('add_ask/', AddUserAskView.as_view(), name="add_ask"), #我要学习
    path('org_home/<int:org_id>/', OrgDetailHome.as_view(), name="org_home"), #机构首页, org_id（哪个机构）
    path('org_course/<int:org_id>/', OrgDetailCourse.as_view(), name="org_course"), #机构首页
    path('org_desc/<int:org_id>/', OrgDescCourse.as_view(), name="org_desc"), #机构介绍
    path('org_teachers/<int:org_id>/', OrgTeachersCourse.as_view(), name="org_teachers"), #机构教师
    path('add_fav/', AddFavView.as_view(), name="add_fav"), #机构收藏,models有机构id，所以不用org_id
    path('teacher_list/',TeacherListView.as_view(),name="teacher_list"),#教师列表
    path('teacher_detail/<int:teacher_id>/', TeacherDetailView.as_view(), name="teacher_detail"), #教师详情页
]
