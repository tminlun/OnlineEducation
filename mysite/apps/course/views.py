from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #分页
from django.shortcuts import render,get_object_or_404
from django.views.generic import View
from operation.models import UserCourse
from .models import Course
# Create your views here.


class CourseListView(View):
    """
    课程列表
    """
    def get(self, request):
        current_list = "course_list"
        all_course = Course.objects.all()#所有的课程
        hot_courses = all_course.order_by("-click_nums")[:3]#最热门的3课程

        #最热门、参与人数；如果不写在分页前面，分页会失效
        sort = request.GET.get("sort", "")
        if sort == "hot":
            all_course = all_course.order_by("-click_nums")
        elif sort == "students":
            all_course = all_course.order_by("-students")
        # 分页功能
        try:
            page = request.GET.get('page', 1)  # 获取n（page=n）,默认显示第一页
        except PageNotAnInteger:
            page = 1  # 出现异常显示第一页
        p = Paginator(all_course, 3, request=request)  # 进行分页，每5个作为一页
        course = p.page(page)  # 获取当前页面

        return render(request, 'course-list.html', {
            "all_course": course, #all_course.object_list
            "current_list": current_list, #当前页面 active
            "sort": sort, #最热门、参与人数
            "hot_courses": hot_courses,#最热门的3课程
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course_detail = get_object_or_404(Course, pk=course_id)#具体的

        user_course = UserCourse.objects.filter(course=course_detail)
        return render(request, 'course-detail.html', {
            "course_detail": course_detail,
            "user_course": user_course,
        })
