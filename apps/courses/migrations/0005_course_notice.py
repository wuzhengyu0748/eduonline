# Generated by Django 2.2 on 2020-02-29 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_coursetag'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='notice',
            field=models.CharField(default='', max_length=300, verbose_name='课程公告'),
        ),
    ]