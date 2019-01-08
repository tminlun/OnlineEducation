# Generated by Django 2.0 on 2019-01-08 14:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0003_auto_20190108_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecomments',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_course', to='course.Course', verbose_name='评论的课程'),
        ),
        migrations.AlterField(
            model_name='coursecomments',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_comment', to='operation.CourseComments', verbose_name='上一级评论'),
        ),
        migrations.AlterField(
            model_name='coursecomments',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_users', to=settings.AUTH_USER_MODEL, verbose_name='回复给谁'),
        ),
        migrations.AlterField(
            model_name='coursecomments',
            name='root',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='root_comment', to='operation.CourseComments', verbose_name='顶级评论'),
        ),
    ]