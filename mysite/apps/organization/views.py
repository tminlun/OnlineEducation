# _*_ encoding:utf-8 _*_
from django.shortcuts import render
from django.views.generic import View
from .models import CourseOrg, CityDict
# Create your views here.


class OrgView(View):
    def get(self,request):
        all_orgs = CourseOrg.objects.all() #所有的机构
        org_nums = all_orgs.count() #所有的机构数量
        all_citys = CityDict.objects.all()#所有的机构城市
        return render(request, 'org-list.html', {
            "all_orgs": all_orgs,
            "all_citys": all_citys,
            "org_nums": org_nums
        })
