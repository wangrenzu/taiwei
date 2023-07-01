# Generated by Django 3.2.9 on 2023-06-10 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0016_product_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='clickDeal',
            field=models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='本场点击成交率'),
        ),
        migrations.AddField(
            model_name='product',
            name='clickExposure',
            field=models.DecimalField(decimal_places=4, max_digits=10, null=True, verbose_name='本场曝光点击率'),
        ),
        migrations.AddField(
            model_name='product',
            name='exposure',
            field=models.IntegerField(null=True, verbose_name='本场曝光量'),
        ),
    ]