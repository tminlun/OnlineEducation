# Generated by Django 2.0 on 2018-12-20 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0010_auto_20181220_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='teacher/default_middile_1.png', upload_to='teacher/%Y%m', verbose_name='老师头像'),
        ),
    ]
