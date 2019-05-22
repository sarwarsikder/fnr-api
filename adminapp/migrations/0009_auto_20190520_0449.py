# Generated by Django 2.2.1 on 2019-05-20 04:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0008_auto_20190516_0909'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='sending_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='buildingplans',
            name='plan_file',
            field=models.FileField(null=True, upload_to='static/assets/building/plan_pdf/'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='file_type',
            field=django_mysql.models.JSONField(default='[]'),
        ),
        migrations.AlterField(
            model_name='flatplans',
            name='plan_file',
            field=models.FileField(null=True, upload_to='static/assets/flat/plan_pdf/'),
        ),
        migrations.CreateModel(
            name='ProjectPlans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('plan_file', models.FileField(null=True, upload_to='static/assets/project/plan_pdf/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_plan_created_by', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adminapp.Projects')),
            ],
            options={
                'db_table': 'project_plans',
            },
        ),
    ]