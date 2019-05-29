# Generated by Django 2.2.1 on 2019-05-28 05:49

from django.db import migrations
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0019_auto_20190528_0418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='file_type',
            field=django_mysql.models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='handworker',
            name='working_type',
            field=django_mysql.models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='followers',
            field=django_mysql.models.JSONField(blank=True, default=dict, null=True),
        ),
    ]