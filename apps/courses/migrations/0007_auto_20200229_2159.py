# Generated by Django 2.2 on 2020-02-29 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_auto_20200229_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='url',
            field=models.CharField(max_length=1000, verbose_name='视频地址'),
        ),
    ]
