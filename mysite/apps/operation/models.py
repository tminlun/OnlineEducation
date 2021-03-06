from datetime import datetime
from django.db import models
from users.models import UserProfile
from course.models import Course
# Create your models here.


#用户咨询
class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name="姓名")
    phone_nums = models.CharField(max_length=11,verbose_name="用户手机号码")
    course_name = models.CharField(max_length=50, verbose_name="课程名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="用户咨询的时间")

    class Meta:
        verbose_name = "用户咨询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


#用户消息表
class UserMessage(models.Model):
    """
        user字段，默认0代表消息是发给所有用户，而不是某个单独的用户；
        可以通过user.id发给特定用户消息
    """
    user = models.IntegerField(default=0,verbose_name="用户s")#数字类型
    message = models.CharField(max_length=500,verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="推送消息时间")

    class Meta:
        verbose_name = "用户消息表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message


# 用户评论
class CourseComments(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="评论的用户")
    course = models.ForeignKey(Course,related_name='comment_course',on_delete=models.CASCADE,verbose_name="评论的课程")
    comment = models.CharField(max_length=200,verbose_name="评论内容")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="评论时间")

    root = models.ForeignKey('self',related_name="root_comment",on_delete=models.CASCADE,null=True,blank=True,verbose_name="顶级评论")
    parent = models.ForeignKey('self',related_name="parent_comment",on_delete=models.CASCADE,null=True,blank=True,verbose_name="上一级评论")#上一级评论在此模型

    reply_to = models.ForeignKey(UserProfile,related_name="reply_users",on_delete=models.CASCADE,null=True,blank=True,verbose_name="回复给谁")

    class Meta:
        verbose_name = "用户评论"
        verbose_name_plural = verbose_name
        ordering = ["-add_time"]

    def __str__(self):
        return "{0}添加：{1}".format(self.user, self.comment)


#UserCourse 用户学习的课程
class UserCourse(models.Model):
    """
    用户学习的课程,可以用到"UserProfile"的字段
    """
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="用户")
    course = models.ForeignKey(Course,on_delete=models.CASCADE,verbose_name="学习的课程")
    add_time = models.DateTimeField(default=datetime.now,verbose_name="学习时间")

    class Meta:
        verbose_name = "用户学习的课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{0}添加课程:'{1}'".format(self.user, self.course)


#Favorite 用户收藏
class UserFavorite(models.Model):
    """
    用户收藏
    """
    favorite_choices = (
        (1, '课程'),
        (2, '机构'),
        (3, '讲师')
    )
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,verbose_name="用户")
    fav_id = models.IntegerField(default=0,verbose_name="收藏id")
    fav_type = models.IntegerField(default=1,choices=favorite_choices,verbose_name="收藏类型(默认为1)")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="收藏的时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

