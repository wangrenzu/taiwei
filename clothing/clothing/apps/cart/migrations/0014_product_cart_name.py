# Generated by Django 3.2.9 on 2023-06-06 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0013_alter_product_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='cart_name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='购物车名称'),
        ),
    ]
