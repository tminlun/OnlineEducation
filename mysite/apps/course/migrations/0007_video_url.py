# Generated by Django 2.0 on 2018-12-25 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_course_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.CharField(default='', max_length=200, verbose_name='访问地址'),
        ),
    ]
