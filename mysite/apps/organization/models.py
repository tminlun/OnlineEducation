from datetime import datetime
from django.db import models

# Create your models here.

class CityDict(models.Model):
    name = models.CharField(max_length=20,verbose_name="城市")
    desc = models.CharField(max_length=200,verbose_name="描述")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="创建时间")

    class Meta:
        verbose_name = '城市'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


#CourseOrg  课程机构基本信息
class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = models.TextField(verbose_name="机构的描述")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to='org/%Y%m',default='org/default.png', verbose_name="机构的封面图")
    address = models.CharField(max_length=150, verbose_name="机构地址")
    city = models.ForeignKey(CityDict, verbose_name='所在城市', on_delete=models.CASCADE,null=True,blank=True)
    add_time = models.DateTimeField(default=datetime.now,verbose_name="时间")

    class Meta:
        verbose_name = "课程机构的基本信息"
        verbose_name_plural = verbose_name


#机构中的老师
class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,on_delete=models.CASCADE, verbose_name="所属机构")
    name = models.CharField(max_length=15, verbose_name="教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    points = models.CharField(max_length=50, verbose_name="公司职位")
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = "机构老师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "[{0}]的教师：{1}".format(self.org, self.name)