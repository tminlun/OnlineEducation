# Generated by Django 2.0 on 2018-12-18 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_auto_20181217_2005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='courseorg',
            name='image',
            field=models.ImageField(blank=True, default='org/default.png', null=True, upload_to='org/%Y%m', verbose_name='机构logo'),
        ),
    ]