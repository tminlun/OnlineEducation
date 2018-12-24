# _*_ encoding:utf-8 _*_
import re
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #分页
from django.shortcuts import render,get_object_or_404
from django.views.generic import View
from django.http import JsonResponse
from operation.models import UserFavorite
from .models import CourseOrg, CityDict
from .forms import UserAskForm
# Create your views here.


class OrgView(View):
    """
    课程机构：
    分页：Paginator
    order_by()：排序
    all_orgs.filter(), 获取出所有的类别在进行筛选，有便于返回筛选的全部列表
    如果是点击全部，就是筛选为空 “ ifequal category '' ”
    ?ct=pxjg&city={{ city_id }}:并查询（筛选）
      为什么用户点击了城市能够显示出，对应列表，因为筛选了当前城市以后，返回了all_orgs给他，
    当他点击了对应的city.id超链接，就返回对应的city.id机构列表：all_orgs = all_orgs.filter(city_id=int(city_id))
    """
    def get(self,request):
        current_list = "org_list"
        all_orgs = CourseOrg.objects.all() #所有的机构
        hot_orgs = all_orgs.order_by("-click_nums")[:3] #（机构排名）对所有的课程点击数进行排序,并取得前3个
        all_citys = CityDict.objects.all()#所有的机构城市

        #机构筛选
        city_id = request.GET.get("city", "") #?city={{ city.id }}
        if city_id:#注意：如果用户点击了筛选才进行筛选
            all_orgs = all_orgs.filter(city_id=int(city_id)) #可以通过CourseOrg来筛选City：CourseOrg自带city_id

        #机构类别筛选
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category) #直接all_orgs筛选，显示出当前的类别

        #学习人数*课程数的排序
        sort = request.GET.get("sort", "") #?sort=students | ?sort=courses
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()  # 所有的机构数量,等对应对象筛选完后再统计

        #分页功能
        try:
            page = request.GET.get('page', 1) #获取n（page=n）,默认显示第一页
        except PageNotAnInteger:
            page = 1 #出现异常显示第一页
        p = Paginator(all_orgs, 5, request=request) #进行分页，每5个作为一页
        orgs = p.page(page) #获取当前页面

        return render(request, 'org-list.html', {
            "all_orgs": orgs,
            "all_citys": all_citys,
            "org_nums": org_nums,
            "city_id": city_id,
            "category": category,
            "hot_orgs": hot_orgs,
            "sort": sort,
            "current_list": current_list,
        })


class AddUserAskView(View):
    """
    我要咨询
    实例化 modelform，如果验证成功，把用户输入的数据放进数据库并保存
    保存成功后返回json 判断是否提交成功，并把错误返回给json
    """
    def post(self, request):
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            """
            判断号码：如果规范保存进数据库(user_ask)，否 则返回错误
            如果这样会出现错误：if p.match(phone_nums): #判断输入是否是一个手机号
                   return phone_nums
                else:
                    raise forms.ValidationError("手机号不规范", code="phone_nums_inval")
            """
            phone_nums = request.POST.get("phone_nums", "")
            REGEX_PHONE_NUMS = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
            p = re.compile(REGEX_PHONE_NUMS)
            if not p.match(phone_nums):  # 判断输入是否是一个手机号
                return JsonResponse({"status": "fail", "msg": "请输入11位数字"})

            # 省去 request.POST.get和实例化，commit=True：可以存储进数据库
            user_ask = userask_form.save(commit=True)
            return JsonResponse({'status': 'success'})
        else:
           return JsonResponse({'status': 'fail', 'msg': '输入错误'}) #'msg': "{}".format(userask_form.errors.values())[11:].strip("()")


class OrgDetailHome(View):
    """
    课程机构首页（不是列表）
    获取具体的机构，同过外键（机构中外键、别的模型外键机构）来反向查询所有的课程、教师
    记住每个课程的机构都是不同的，外键不同
    org_base可以用org-detail-homepage的对象
    """
    def get(self, request, org_id):
        current_page = 'home' #前端active（选中）判断是否为当前页面
        detail_org = get_object_or_404(CourseOrg, pk=int(org_id)) #获取具体的机构
        all_course = detail_org.course_set.all()[:3] #反向查询所有的课程
        all_teacher = detail_org.teacher_set.all()[:1] #反向查询所有的教师
        """用户是否收藏，has_fav = False：默认为没有has_fav"""
        has_fav = False
        if request.user.is_authenticated:#登录后才能收藏，因为如果数据库有记录，而不是具体的收藏人，就会默认转为已收藏
            if UserFavorite.objects.filter(user=request.user, fav_id=int(detail_org.pk), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-homepage.html',{
            "all_course": all_course,
            "all_teacher": all_teacher,
            "detail_org": detail_org, # 为了显示org_base具体机构的图片
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgDetailCourse(View):
    """
    课程机构课程
    """
    def get(self, request, org_id):
        current_page = 'course'  # 前端active（选中）判断是否为当前页面
        detail_org = get_object_or_404(CourseOrg, pk=int(org_id)) #获取具体的机构
        all_course = detail_org.course_set.all()#反向查询所有的课程
        has_fav = False
        if request.user.is_authenticated:#判断是否为当前用户
            if UserFavorite.objects.filter(user=request.user, fav_id=int(detail_org.pk), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-course.html',{
            "all_course": all_course,
            "detail_org": detail_org, # 为了显示org_base具体机构的图片
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgDescCourse(View):
    """
    机构介绍
    """
    def get(self, request, org_id):
        current_page = 'desc'  # 前端active（选中）判断是否为当前页面
        detail_org = get_object_or_404(CourseOrg, pk=int(org_id)) #获取具体的机构
        has_fav = False
        if request.user.is_authenticated:  # 判断是否为当前用户
            if UserFavorite.objects.filter(user=request.user, fav_id=int(detail_org.pk), fav_type=2):
                has_fav = True
        return render(request, 'org-detail-desc.html',{
            "detail_org": detail_org, # 为了显示org_base具体机构的图片
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgTeachersCourse(View):
    """
    机构教师
    """
    def get(self, request, org_id):
        current_page = 'teachers'  # 前端active（选中）判断是否为当前页面
        detail_org = get_object_or_404(CourseOrg, pk=int(org_id)) #获取具体的机构
        all_teachers = detail_org.teacher_set.all()
        has_fav = False #用户未收藏
        if request.user.is_authenticated:  # 判断是否为当前用户
            if UserFavorite.objects.filter(user=request.user, fav_id=int(detail_org.pk), fav_type=2):
                has_fav = True#用户已收藏
        return render(request, 'org-detail-teachers.html',{
            "detail_org": detail_org, # 为了显示org_base具体机构的图片
            "current_page": current_page,
            "all_teachers": all_teachers,
            "has_fav": has_fav,
        })


class AddFavView(View):
    """
    机构收藏、取消收藏
    逻辑：获取fav_id、fav_type（都是数字字段）.获取不到返回0
    如果没有登录，返回json错误，前端会重定向登录页面
    筛选（哪个用户，当前类型，哪个类型的id）数据库有没有"收藏"数据，如果有（已收藏），表明用户要取消收藏
    如果没有数据，即收藏；注：如果获取不到"fav_id、fav_type", 不进行收藏，给报错
    """
    def post(self, request):
        fav_id = request.POST.get("fav_id", 0)
        fav_type = request.POST.get("fav_type", 0)
        if not request.user.is_authenticated:
            return JsonResponse({"status": "fail", "msg": "用户未登录"})
        # exist_record是否存在记录
        exist_record = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_record:
            """取消收藏"""
            exist_record.delete()
            return JsonResponse({"status": "success", "msg": "收藏"})
        else:
            """收藏"""
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                return JsonResponse({"status": "success", "msg": "已收藏"})
            else:
                return JsonResponse({"status": "fail", "msg": "收藏出错"})