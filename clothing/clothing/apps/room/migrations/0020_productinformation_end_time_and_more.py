# Generated by Django 4.2.2 on 2023-07-08 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("room", "0019_productinformation_pay_combo_cnt"),
    ]

    operations = [
        migrations.AddField(
            model_name="productinformation",
            name="end_time",
            field=models.DateTimeField(null=True, verbose_name="讲解结束时间"),
        ),
        migrations.AddField(
            model_name="productinformation",
            name="start_time",
            field=models.DateTimeField(null=True, verbose_name="讲解开始时间"),
        ),
    ]