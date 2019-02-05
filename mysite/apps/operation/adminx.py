import xadmin
from .models import UserAsk,UserMessage,CourseComments,UserCourse,UserFavorite

class UserAskAdmin(object):
    '''用户表单我要学习'''

    list_display = ['name', 'phone_nums', 'course_name', 'add_time']
    search_fields = ['name', 'phone_nums', 'course_name']
    list_filter = ['name', 'phone_nums', 'course_name', 'add_time']
    model_icon = 'fas fa-hard-hat'


class UserMessageAdmin(object):
    '''用户消息后台'''
    list_display = ['user', 'message', 'has_read', 'add_time']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read', 'add_time']
    model_icon = 'fas fa-sms'


class CourseCommentsAdmin(object):
    '''用户评论后台'''

    list_display = ['user', 'course', 'comment', 'add_time']
    search_fields = ['user', 'course', 'comment']
    list_filter = ['user', 'course', 'comment', 'add_time']
    model_icon = 'fas fa-comments'


class UserCourseAdmin(object):
    '''用户学习课程'''
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']
    model_icon = 'fas fa-graduation-cap'


class UserFavoriteAdmin(object):
    """用户收藏后台"""

    list_display = ['user', 'fav_id', 'fav_type', 'add_time']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type', 'add_time']
    model_icon = 'fas fa-star'


# 将后台管理器与models进行关联注册。
xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)