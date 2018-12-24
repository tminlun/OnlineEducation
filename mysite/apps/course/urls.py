# _*_ encoding:utf-8 _*_
#__file__ : urls.py 
__author__: '田敏伦'
__date__: '2018/12/24 0024 19:21'

from django.urls import path
from .views import CourseListView, CourseDetailView

app_name = "course"
urlpatterns = [
    path('course_list/', CourseListView.as_view(), name="course_list"),#课程公开课
    path('course_detail/<int:course_id>', CourseDetailView.as_view(), name="course_detail"),#课程详情
]
