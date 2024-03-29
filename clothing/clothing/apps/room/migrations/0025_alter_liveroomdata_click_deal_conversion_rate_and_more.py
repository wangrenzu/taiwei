# Generated by Django 4.2.2 on 2023-07-14 11:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("room", "0024_liveroomdata_ad_deal_orders"),
    ]

    operations = [
        migrations.AlterField(
            model_name="liveroomdata",
            name="click_deal_conversion_rate",
            field=models.DecimalField(
                decimal_places=4, max_digits=10, null=True, verbose_name="点击成交转化率"
            ),
        ),
        migrations.AlterField(
            model_name="liveroomdata",
            name="product_ctr",
            field=models.DecimalField(
                decimal_places=4, max_digits=10, null=True, verbose_name="商品千次曝光成交"
            ),
        ),
    ]
