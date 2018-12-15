from datetime import datetime
from django.db import models

# Create your models here.
#课程表
class Course(models.Model):
    #课程难度
    degree_choices = (
        ('cj', '初级'),
        ('zj', '中级'),
        ('gj', '高级')
    )
    name = models.CharField(max_length=15,verbose_name="课程名")
    desc = models.CharField(max_length=200,verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程详情")
    degree = models.CharField(max_length=10, choices=degree_choices,verbose_name="难度")
    learn_times = models.IntegerField(default=0,verbose_name='学习时长(分钟)')
    students = models.IntegerField(default=0,verbose_name="学习人数")
    fav_nums = models.IntegerField(default=0,verbose_name="收藏人数")
    image = models.ImageField(upload_to="course/%Y%m",default="course/default.png",verbose_name="封面图")
    click_nums = models.IntegerField(default=0,verbose_name="点击数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")#default和auto_now有冲突

    class Meta:
        verbose_name = "课程"
        verbose_name_plural = verbose_name

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

