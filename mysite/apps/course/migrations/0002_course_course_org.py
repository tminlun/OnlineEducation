# Generated by Django 2.0 on 2018-12-20 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0004_auto_20181218_1647'),
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_org',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='organization.CourseOrg'),
        ),
    ]
