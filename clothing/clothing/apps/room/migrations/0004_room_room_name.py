# Generated by Django 3.2.9 on 2023-06-08 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('room', '0003_auto_20230608_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='room_name',
            field=models.CharField(max_length=10, null=True, verbose_name='直播间名称'),
        ),
    ]