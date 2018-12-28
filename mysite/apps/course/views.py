from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #分页
from django.shortcuts import render,get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from operation.models import UserCourse
from operation.models import UserFavorite, CourseComments
from .models import Course, CourseResource
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
        current_list = "course_list"
        course_detail = get_object_or_404(Course, pk=course_id)#具体的

        # 每一次点击（点击数）加1
        if not request.COOKIES.get("%s_pk" % course_detail.pk):
            course_detail.click_nums += 1
            course_detail.save()

        """前端的ajax可以使用以前写的收藏代码: url:"{% url 'org:add_fav' %}",因为逻辑是一样的
        {% if has_org_fav  %}已收藏{% else %}收藏{% endif %}判断是否收藏，
            如果有has_course_fav则显示"已收藏"，否 显示"收藏"
            (如果没有加{% else %}如果没有收藏显示不出来)
        """
        has_course_fav = False
        has_org_fav = False
        # 必须是用户已登录我们才需要判断。
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_detail.pk, fav_type=1):
                has_course_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course_detail.course_org.pk, fav_type=2):
                has_org_fav = True

        # 得到相关课程：1、得到页面的课程对象，再对Coures进行筛选
        tag = course_detail.tag
        if tag:  # 查询此课程是否相关课程
            #必须从1开始不然会推荐自己为相关课程
            relate_courses = Course.objects.filter(tag=tag)[1:2]
        else:
            relate_courses = []  # 因为前端是for循环，所有要返回数组
        response = render(request, 'course-detail.html', {
            "course_detail": course_detail,
            "current_list": current_list,  # 当前页面 active
            "relate_courses": relate_courses,
            "has_course_fav": has_course_fav,#课程收藏
            "has_org_fav": has_org_fav,#机构收藏
        })
        response.set_cookie("%s_pk" % course_detail.pk, 'true')
        return response


class CourseInfoView(View):
    """
    课程信息：course_id：具体课程
    """
    def get(self, request, course_id):
        current_list = "course_list"
        course_detail = get_object_or_404(Course, pk=course_id)
        all_resources = CourseResource.objects.filter(course=course_detail) #哪个课程的资源
        return render(request, "course-video.html", {
            "current_list": current_list,  # 当前页面 active
            "course_detail": course_detail,
            "course_resources": all_resources, #哪个课程的资源
        })


class CourseCommentView(View):
    def get(self, request, course_id):
        current_list = "course_list"
        course_detail = get_object_or_404(Course, pk=course_id)
        all_course_comment = CourseComments.objects.filter(course=course_detail)#所有的评论
        return render(request, 'course-comment.html',{
            "current_list": current_list, #传给base
            "course_detail": course_detail,
            "all_course_comment": all_course_comment,
        })


class AddCommentView(View):
    def post(self, request):
        obj_id = request.POST.get('course_id', 0)
        comments = request.POST.get('comments', '')
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'fail', 'msg': '用户未登录'})
        #实例化
        course_comments = CourseComments()
        #如果获取有效的
        if int(obj_id) > 0 and comments != '':
            course_comments.user = request.user
            course_comments.course = Course.objects.get(pk=int(obj_id)) #评论的对象
            course_comments.comment = comments
            course_comments.save()
            return JsonResponse({'status': 'success', 'msg': '评论成功'})
        else:
            return JsonResponse({'status': 'fail', 'msg': '评论失败'})

