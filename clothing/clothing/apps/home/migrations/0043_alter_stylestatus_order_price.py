# Generated by Django 4.2.2 on 2023-08-16 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0042_remove_stylestatus_is_other_remove_stylestatus_num_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stylestatus",
            name="order_price",
            field=models.IntegerField(null=True, verbose_name="订单金额"),
        ),
    ]
