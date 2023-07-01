from django.db import models


# Create your models here.
class Product(models.Model):
    commodity_code = models.CharField(verbose_name='款号', null=True, max_length=255, blank=True)
    product_name = models.CharField(verbose_name='货品名', max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, verbose_name='图片', null=True, blank=True)
    order_quantity = models.IntegerField(verbose_name='订购量', null=True, blank=True)
    workshop_quantity = models.CharField(max_length=255, verbose_name='车间规格量', null=True, blank=True)
    workshop_quantity_num = models.IntegerField(verbose_name="车间可卖量", null=True)
    post_processing_quantity = models.CharField(max_length=255, verbose_name='后道规格量', null=True, blank=True)
    post_processing_quantity_num = models.IntegerField(verbose_name="后道可卖量", null=True)
    taiwei_yifa_moyajia_quantity = models.CharField(max_length=255, verbose_name='泰维+意法+茉雅规格量', null=True,
                                                    blank=True)
    taiwei_yifa_moyajia_quantity_num = models.IntegerField(verbose_name="泰维+意法+茉雅可卖量", null=True)
    pending_and_in_transit = models.IntegerField(verbose_name='待发+在途', null=True, blank=True)
    cancelled = models.IntegerField(verbose_name='取消', null=True, blank=True)
    successful = models.IntegerField(verbose_name='成功', null=True, blank=True)
    returned = models.IntegerField(verbose_name='退回', null=True, blank=True)
    price = models.IntegerField(verbose_name='订单应付金额', null=True)
    live_deal_conversion_rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='直播间成交转化率',
                                                    null=True, blank=True)
    exposure_click_rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='曝光点击率', null=True,
                                              blank=True)
    max_exposure_quantity = models.IntegerField(verbose_name='最大曝光量', null=True, blank=True)
    avg_live_exposure_count = models.IntegerField(verbose_name='3天平均曝光量', null=True, blank=True)
    prediction = models.IntegerField(verbose_name='预测销量', null=True, blank=True)
    prediction_money = models.IntegerField(verbose_name='预测金额', null=True, blank=True)
    cart_name = models.CharField(max_length=20, verbose_name='购物车名称', null=True, blank=True)
    source = models.CharField(max_length=20, verbose_name='来源', null=True, blank=True)
    exposure = models.IntegerField(verbose_name='本场曝光量', null=True)
    clickExposure = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='本场曝光点击率', null=True)
    clickDeal = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='本场点击成交率', null=True)

    class Meta:
        verbose_name = '购物车商品'
        verbose_name_plural = '购物车商品'
        db_table = 'taiwei_product'

    def __str__(self):
        return self.commodity_code
