# Generated by Django 2.0 on 2019-01-08 13:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('operation', '0002_auto_20181228_2136'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecomments',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_comment', to='operation.CourseComments', verbose_name='上一级评论'),
        ),
        migrations.AddField(
            model_name='coursecomments',
            name='reply_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reply_users', to=settings.AUTH_USER_MODEL, verbose_name='回复给谁'),
        ),
        migrations.AddField(
            model_name='coursecomments',
            name='root',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='root_comment', to='operation.CourseComments', verbose_name='顶级评论'),
        ),
        migrations.AlterField(
            model_name='coursecomments',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='评论的用户'),
        ),
    ]
