# Generated by Django 2.0 on 2018-12-20 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0002_course_course_org'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, default='course/default.png', null=True, upload_to='course/%Y%m', verbose_name='封面图'),
        ),
    ]
