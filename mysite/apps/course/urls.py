# _*_ encoding:utf-8 _*_
#__file__ : urls.py 
__author__: '田敏伦'
__date__: '2018/12/24 0024 19:21'

from django.urls import path
from .views import CourseListView, CourseDetailView, CourseInfoView, CourseCommentView, AddCommentView,VideoPlayView,ReplyCommentView

app_name = "course"
urlpatterns = [
    path('course_list/', CourseListView.as_view(), name="course_list"),#课程公开课
    path('course_detail/<int:course_id>', CourseDetailView.as_view(), name="course_detail"),#课程详情
    path('course_info/<int:course_id>', CourseInfoView.as_view(), name="course_info"),#课程信息（章节、视频）
    path('course_comment/<int:course_id>', CourseCommentView.as_view(), name="course_comment"),#课程评论
    path('add_comment/', AddCommentView.as_view(), name="add_comment"),#评论功能
    path('reply_comment/', ReplyCommentView.as_view(), name="reply_comment"),#回复功能
    path('video_play/<int:video_id>', VideoPlayView.as_view(), name="video_play"),#课程视频
]
