# Generated by Django 2.2.1 on 2019-05-21 04:43

import adminapp.models
from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0010_auto_20190520_0512'),
    ]

    operations = [
        migrations.AddField(
            model_name='buildingplans',
            name='file_type',
            field=models.CharField(default='pdf', max_length=45),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='flatplans',
            name='file_type',
            field=models.CharField(default='pdf', max_length=45),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='projectplans',
            name='file_type',
            field=models.CharField(default='pdf', max_length=45),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='users',
            name='current_activity',
            field=django_mysql.models.JSONField(default=adminapp.models.my_default),
        ),
        migrations.AlterField(
            model_name='buildingplans',
            name='plan_file',
            field=models.FileField(null=True, upload_to='static/assets/building/plans/'),
        ),
        migrations.AlterField(
            model_name='flatplans',
            name='plan_file',
            field=models.FileField(null=True, upload_to='static/assets/flat/plans/'),
        ),
        migrations.AlterField(
            model_name='projectplans',
            name='plan_file',
            field=models.FileField(null=True, upload_to='static/assets/project/plans/'),
        ),
    ]
