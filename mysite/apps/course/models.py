from datetime import datetime
from django.db import models
from organization.models import CourseOrg
# Create your models here.


#课程表
class Course(models.Model):
    """课程难度"""
    degree_choices = (
        #在模板显示值：{{ hot_course.get_degree_display }}
        ('cj', '初级'),
        ('zj', '中级'),
        ('gj', '高级')
    )
    course_org = models.ForeignKey(CourseOrg, null=True,blank=True, on_delete=models.CASCADE)#CourseOrg可反向查询它
    name = models.CharField(max_length=15,verbose_name="课程名")
    desc = models.CharField(max_length=200,verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    degree = models.CharField(max_length=10, choices=degree_choices,verbose_name="难度")
    learn_times = models.IntegerField(default=0,verbose_name='学习时长(分钟)')
    students = models.IntegerField(default=0,verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0,verbose_name="收藏人数")
    image = models.ImageField(upload_to="course/%Y%m",default="course/default.png",verbose_name="封面图",null=True,blank=True)
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    category = models.CharField(default="后端开发",max_length=20, verbose_name="课程类别")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")#default和auto_now有冲突

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name
        ordering = ['-add_time']

    #章节数（一个课程有多少个章节）
    def get_lesson_nums(self):
        """反向查询所有的章节数，（章节有了此外键）"""
        return self.lesson_set.all().count()

    #课程学习的用户
    def get_user_course(self):
        return self.usercourse_set.all()[:5]

    #教师数量
    def get_teacher_nums(self):
        """当前模型指向外键，则（self.course_org）就获取到了（外键的所有”字段“和”外键的外键字段“）"""
        return self.course_org.teacher_set.all().count()

    def __str__(self):
        return self.name


#课程的章节
class Lesson(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name="哪个课程")
    name = models.CharField(max_length=100, verbose_name="章节名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="章节添加时间")

    class Meta:
        verbose_name = "课程的章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "《{0}》的第{1}章节".format(self.course, self.name)


#（视频）章节里面有视频
class Video(models.Model):
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE,verbose_name="章节")
    name = models.CharField(max_length=100, verbose_name="视频名")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加视频时间")

    class Meta:
        verbose_name = "章节的视频"
        verbose_name_plural = verbose_name


#课程资源
class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name="资源名")
    download = models.FileField(upload_to="course/resource/%Y%m",verbose_name="资源文件")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

