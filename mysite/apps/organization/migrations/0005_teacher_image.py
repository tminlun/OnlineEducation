# Generated by Django 2.0 on 2018-12-20 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20181218_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='image',
            field=models.ImageField(default='', upload_to='teacher/%Y%m', verbose_name='老师头像'),
        ),
    ]