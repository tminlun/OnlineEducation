# Generated by Django 2.0 on 2019-01-27 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_course_teachers'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_banner',
            field=models.BooleanField(default=False, verbose_name='是否为轮播图'),
        ),
    ]
