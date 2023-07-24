# Generated by Django 4.2.2 on 2023-07-14 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("room", "0020_productinformation_end_time_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="LiveRoomData",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "datetime",
                    models.DateTimeField(auto_now=True, verbose_name="时间点-月日时秒"),
                ),
                ("total_exposure", models.IntegerField(null=True, verbose_name="总曝光")),
                (
                    "enter_room_ad",
                    models.IntegerField(null=True, verbose_name="进入直播间-广告"),
                ),
                (
                    "click_product_ad",
                    models.IntegerField(null=True, verbose_name="点击商品-广告"),
                ),
                (
                    "create_order_ad",
                    models.IntegerField(null=True, verbose_name="创建订单-广告"),
                ),
                (
                    "deal_order_ad",
                    models.IntegerField(null=True, verbose_name="成交订单-广告"),
                ),
                (
                    "enter_room_organic",
                    models.IntegerField(null=True, verbose_name="进入直播间-自然"),
                ),
                (
                    "click_product_organic",
                    models.IntegerField(null=True, verbose_name="点击商品-自然"),
                ),
                (
                    "create_order_organic",
                    models.IntegerField(null=True, verbose_name="创建订单-自然"),
                ),
                (
                    "deal_order_organic",
                    models.IntegerField(null=True, verbose_name="成交订单-自然"),
                ),
                (
                    "product_sequence",
                    models.IntegerField(null=True, verbose_name="商品序号"),
                ),
                (
                    "product_code",
                    models.CharField(max_length=255, null=True, verbose_name="商品款号"),
                ),
                (
                    "ad_gmv",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, null=True, verbose_name="广告GMV"
                    ),
                ),
                (
                    "expenditure",
                    models.DecimalField(
                        decimal_places=2, max_digits=10, null=True, verbose_name="消耗"
                    ),
                ),
                (
                    "product_ctr",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=5,
                        null=True,
                        verbose_name="商品千次曝光成交",
                    ),
                ),
                (
                    "ad_settlement_orders",
                    models.IntegerField(null=True, verbose_name="广告结算订单数"),
                ),
                (
                    "ad_settlement_cost",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="广告结算成本",
                    ),
                ),
                (
                    "click_deal_conversion_rate",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=5,
                        null=True,
                        verbose_name="点击成交转化率",
                    ),
                ),
                (
                    "product_exposure_users",
                    models.IntegerField(null=True, verbose_name="商品曝光人数"),
                ),
                (
                    "product_click_users",
                    models.IntegerField(null=True, verbose_name="商品点击人数"),
                ),
                (
                    "cumulative_deal_amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=10,
                        null=True,
                        verbose_name="累计成交金额",
                    ),
                ),
                (
                    "cumulative_deal_orders",
                    models.IntegerField(null=True, verbose_name="累计成交订单数"),
                ),
            ],
            options={
                "verbose_name": "每5秒直播间数据",
                "verbose_name_plural": "每5秒直播间数据",
                "db_table": "taiwei_room_second_5",
            },
        ),
    ]