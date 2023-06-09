# Generated by Django 3.2.9 on 2023-06-05 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0008_product_avg_live_exposure_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='prediction',
            field=models.IntegerField(blank=True, null=True, verbose_name='预测销量'),
        ),
        migrations.AddField(
            model_name='product',
            name='prediction_money',
            field=models.FloatField(blank=True, null=True, verbose_name='预测金额'),
        ),
    ]
