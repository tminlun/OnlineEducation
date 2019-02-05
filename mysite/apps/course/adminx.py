import xadmin
from .models import Course,Lesson,Video,CourseResource, BannerCourse


class LessonNest(object):
    """同一个models注册两个管理器"""
    model = Lesson
    extra = 0


class VideoNest(object):
    """同一个models注册两个管理器"""
    model = Video
    extra = 0


class CourseAdmin(object):
    """课程"""

    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students','fav_nums','click_nums','get_lesson_nums','go_to']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']

    # detail就是要显示为富文本的字段名
    style_fields = {"detail": "ueditor"}

    model_icon = 'fab fa-blogger'

    # 正序排序点击数！
    ordering = ['-click_nums']

    # 设置此字段为只读状态（不可编辑）
    readonly_fields = ['fav_nums', 'click_nums']

    #一个models编辑两个models
    inlines = [LessonNest]

    #可以自接在列表修改
    list_editable = ['fav_nums', 'degree', 'name']

    # refresh_times = [3, 5] #每3秒刷新一次

    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        """在保存课程时统计具体机构的课程数量给机构的课程数量"""
        obj = self.new_obj #当前的对象
        obj.save() #保存课程时
        if obj.course_org is not None:
            course_org = obj.course_org #通过外键获取当前课程的机构
            course_org.course_nums = Course.objects.filter(course_org=course_org).count() #统计到org课程数
            course_org.save()


class BannerCourseAdmin(object):
    """同一模型分类管理"""

    list_display = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students','fav_nums','click_nums']
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_times', 'students']
    model_icon = 'fab fa-blogger'
    ordering = ['-click_nums'] #正序排序点击数！
    readonly_fields = ['fav_nums', 'click_nums'] #设置此字段为只读状态（不可编辑）
    inlines = [LessonNest]

    def queryset(self):
        """继承BannerCourseAdmin，进行筛选（is_banner）"""
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


class LessonAdmin(object):
    '''章节'''

    list_display = ['course', 'name', 'add_time']
    # 搜索
    search_fields = ['course', 'name']
    #过滤：course__name：后台显示Course的name字段
    list_filter = ['course__name', 'name', 'add_time']
    model_icon = 'fas fa-angle-down'


class VideoAdmin(object):
    '''视频'''

    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']
    model_icon = 'fas fa-video'


class CourseResourceAdmin(object):
    '''课程资源'''

    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download','add_time']
    model_icon = 'fab fa-internet-explorer'


# 将管理器与model进行注册关联
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)