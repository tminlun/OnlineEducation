# _*_ encoding:utf-8 _*_
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger #分页
from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse
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
        all_orgs = CourseOrg.objects.all() #所有的机构
        hot_orgs = all_orgs.order_by("-click_nums")[:3] #（机构排名）对所有的课程点击数进行排序,并取得前3个
        all_citys = CityDict.objects.all()#所有的机构城市

        #机构筛选
        city_id = request.GET.get("city", "") #?city={{ city.id }}
        if city_id:#注意：如果用户点击了筛选才进行筛选
            all_orgs = all_orgs.filter(city_id=int(city_id)) #当传过来的city_id为1，就筛选city id=1的所有机构列表
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
            user_ask = userask_form.save(commit=True) #省去 request.POST.get和实例化，commit=True：可以存储进数据库
            return JsonResponse({'status': 'success'})
        else:
           return JsonResponse({'status':'fail','msg':'输入错误'})
