# Generated by Django 4.2.2 on 2023-07-01 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0029_alter_newstyle_options"),
    ]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="data_time",
            field=models.DateField(null=True, verbose_name="上传日期"),
        ),
    ]
