from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #分页
from django.shortcuts import render,get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from django.db.models import Q
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin
from users.models import UserProfile
from .models import Course, CourseResource, Video
# Create your views here.


class CourseListView(View):
    """
    课程列表
    """
    def get(self, request):

        all_course = Course.objects.all()#所有的课程
        hot_courses = all_course.order_by("-click_nums")[:3]#最热门的3课程

        #全局搜索
        search_keywords = request.GET.get('keywords', '')#获取用户输入的值]
        if search_keywords:#如果获取的了
            #进行Q查询,包含（__icontains：加了i则不区分大小写）,查询完毕返回值（all_course）
            all_course = all_course.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords)
                                           | Q(detail__icontains=search_keywords)
                                           )


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

            "sort": sort, #最热门、参与人数
            "hot_courses": hot_courses,#最热门的3课程
        })


class CourseDetailView(View):

    def get(self, request, course_id):

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

            "relate_courses": relate_courses,
            "has_course_fav": has_course_fav,#课程收藏
            "has_org_fav": has_org_fav,#机构收藏
        })
        response.set_cookie("%s_pk" % course_detail.pk, 'true')
        return response


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程具体信息：course_id：具体课程
    逻辑：1、current_list = "course_list"表示当前页（active）
    2、获取一个具体对象；3、获取所有的课程资源
    4、该同学还学过:（1）获取该课用户所有id（2）获取该课的同学学过的所有课程 （3）取出这些课程id得到具体的课程信息
    """

    def get(self, request, course_id):

        course_detail = get_object_or_404(Course, pk=course_id)
        all_resources = CourseResource.objects.filter(course=course_detail) #哪个课程的资源

        #当前用户和学习课程关联（实例化用户学习）
        user_courses = UserCourse.objects.filter(user=request.user, course=course_detail)
        if not user_courses:
            user_course = UserCourse(user=request.user, course=course_detail)
            user_course.save()

        # 相关课程推荐
        # 找到学习这门课的所有用户
        user_courses = UserCourse.objects.filter(course=course_detail)
        # 找到学习这门课的所有用户的id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 通过所有用户的id,找到所有用户学习过的所有过程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        # 通过所有课程的id,找到所有的课程，按点击量去五个
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        return render(request, "course-video.html", {

            "course_detail": course_detail,
            "course_resources": all_resources, #哪个课程的资源
            "relate_courses": relate_courses,#该课的同学还学过
        })


class CourseCommentView(LoginRequiredMixin, View):
    """
    评论页面展示
    """
    def get(self, request, course_id):
        current_list = "course_list"
        course_detail = get_object_or_404(Course, pk=course_id)
        all_resources = CourseResource.objects.filter(course=course_detail)  # 哪个课程的资源
        all_course_comment = CourseComments.objects.filter(course=course_detail,root=None)#所有的评论
        # 相关课程推荐
        # 找到学习这门课的所有用户
        user_courses = UserCourse.objects.filter(course=course_detail)
        # 找到学习这门课的所有用户的id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 通过所有用户的id,找到所有用户学习过的所有过程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        # 通过所有课程的id,找到所有的课程，按点击量去五个
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]
        return render(request, 'course-comment.html', {
            "current_list": current_list, #传给base
            "course_detail": course_detail,
            "all_course_comment": all_course_comment,
            "all_resources": all_resources,
            "relate_courses": relate_courses,
        })


def Success(msg):
    """ajax成功"""
    data = {}
    data['status'] = 'success'
    data['msg'] = msg
    return JsonResponse(data)


def Fail(msg):
    """ajax失败"""
    data = {}
    data['status'] = 'fail'
    data['msg'] = msg
    return JsonResponse(data)


class AddCommentView(View):
    """
    评论功能
    """
    def post(self, request):
        obj_id = request.POST.get('course_id', 0) #对象pk
        comments = request.POST.get('comments', '') #评论内容
        if not request.user.is_authenticated:
            return Fail('用户未登录')
        #实例化
        course_comments = CourseComments()
        #如果获取有效的
        if int(obj_id) > 0 and comments != '':
            course_comments.user = request.user
            course_comments.course = Course.objects.get(pk=int(obj_id)) #评论的对象
            course_comments.comment = comments
            course_comments.save()
            return Success('评论成功')
        else:
            return Fail('评论失败')


class ReplyCommentView(View):
    """回复功能"""
    def post(self,request):

        root_id = int(request.POST.get('root_comment_id', 0))#顶级评论的id
        reply_id = int(request.POST.get('reply_comment_id', 0))#上一级回复的id
        reply_user_id = int(request.POST.get('reply_user_id', 0))#上一级回复user的id
        course_id = request.POST.get('course_id', 0)  # 课程id

        root_comment_text = request.POST.get('comment', '')#回复顶级评论的内容
        ptn_text = request.POST.get('ptn', '')#回复回复评论的内容


        try:
            root_id = CourseComments.objects.get(pk=root_id)#获取"一个"评论对象（顶级评论）
            reply_id = CourseComments.objects.get(pk=reply_id)
            reply_user_id = UserProfile.objects.get(pk=reply_user_id) #回复给谁
        except:
            return Fail('回复失败')

        #回复内容传递给数据库
        course_comment = CourseComments()
        course_comment.user = request.user #回复的作者
        course_comment.course = Course.objects.get(pk=course_id)
        course_comment.root = root_id
        course_comment.parent = reply_id
        course_comment.reply_to = reply_user_id
        if ptn_text == '':#如果回复评论的内容为空，则把回复顶级内容赋值给评论内容
            if root_comment_text == '':#如果回复顶级内容为空，抛出错误
                return Fail('回复不能为空')
            course_comment.comment = root_comment_text
        else:
            if ptn_text == '':#如果回复回复评论内容为空，抛出错误
                return Fail('回复不能为空')
            course_comment.comment = ptn_text
        course_comment.save()
        return Success('评论成功') #坑，保存数据库后，记得返回ajax成功信息使得刷新页面


class VideoPlayView(View):
    """课程播放"""
    def get(self, request, video_id):
        current_list = "course_list"
        video = Video.objects.get(pk=int(video_id))

        course_detail = video.lesson.course# 通过外键找到章节再找到视频对应的课程

        # 相关课程推荐
        # 找到学习这门课的所有用户
        user_courses = UserCourse.objects.filter(course=course_detail)
        # 找到学习这门课的所有用户的id
        user_ids = [user_course.user_id for user_course in user_courses]
        # 通过所有用户的id,找到所有用户学习过的所有过程
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
        # 取出所有课程id
        course_ids = [all_user_course.course_id for all_user_course in all_user_courses]
        # 通过所有课程的id,找到所有的课程，按点击量去五个
        relate_courses = Course.objects.filter(id__in=course_ids).order_by("-click_nums")[:5]

        # 资源
        all_resources = CourseResource.objects.filter(course=course_detail)
        return render(request, 'course-play.html', {
            "current_list": current_list,
            'course_detail': course_detail,
            'all_resources': all_resources,
            'relate_courses': relate_courses,
            'video': video,
        })