# Generated by Django 2.2.1 on 2019-05-09 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adminapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='resetpassword',
            name='expired_at',
            field=models.DateTimeField(default=None),
        ),
    ]
