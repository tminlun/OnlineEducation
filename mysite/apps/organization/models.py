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
        """在后台添加了一个对象，显示出添加 name；如果不重构添加了对象时候只会显示obj对象"""
        return self.name


#CourseOrg  机构基本信息
class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = models.TextField(verbose_name="机构的描述")
    #因为没有设置可以为空，是我们要设置默认值
    category = models.CharField(verbose_name="机构类别",default="pxjg",max_length=20, choices=(("pxjg","培训机构"),("gr","个人"),("gx","高校")))
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to='org/%Y%m',default='org/default.png', verbose_name="机构logo",null=True,blank=True)
    address = models.CharField(max_length=150, verbose_name="机构地址")
    #在数据库此字段为：city_id，才能够筛选外键
    city = models.ForeignKey(CityDict, verbose_name='所在城市', on_delete=models.CASCADE,null=True,blank=True)
    students = models.IntegerField(verbose_name="学习人数", default=0)
    course_nums = models.IntegerField(verbose_name="课程数", default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="时间")

    class Meta:
        verbose_name = "课程机构的基本信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        """添加对象显示出name"""
        return self.name

    def descs(self):
        if len(str(self.desc)) > 65:
            return "{}...".format(str(self.desc))[0:65]
        else:
            return self.desc

#机构中的老师
class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg,on_delete=models.CASCADE, verbose_name="所属机构")
    name = models.CharField(max_length=15, verbose_name="教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    points = models.CharField(max_length=50, verbose_name="公司职位")
    click_nums = models.IntegerField(default=0, verbose_name='点击数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏数')
    image = models.ImageField(default="teacher/default_middile_1.png", verbose_name="老师头像",max_length=100,upload_to="teacher/%Y%m")
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        verbose_name = "机构老师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "[{0}]的教师：{1}".format(self.org, self.name)