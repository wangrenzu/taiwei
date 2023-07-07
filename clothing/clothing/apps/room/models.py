from django.db import models


# Create your models here.

class Room(models.Model):
    product_id = models.IntegerField(verbose_name='商品序号')
    code = models.CharField(max_length=30, verbose_name='款号', null=True)
    img = models.CharField(max_length=255, verbose_name='图片', null=True)
    characteristic = models.CharField(max_length=255, verbose_name='特征', null=True)
    exposure = models.IntegerField(verbose_name='曝光量', null=True)
    clickExposure = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='曝光点击率', null=True)
    clickDeal = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='点击成交率', null=True)
    salesPrice = models.FloatField(verbose_name='销售金额', null=True)
    salesNum = models.IntegerField(verbose_name='件数', null=True)
    date_time = models.DateField(verbose_name='直播日期', auto_now=True)
    session = models.CharField(max_length=10, verbose_name='第几场直播', default='第一场')
    room_name = models.CharField(max_length=10, verbose_name='直播间名称', null=True)
    order_number = models.IntegerField(verbose_name='广告结算订单数', null=True)
    order_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='广告结算订单率',
                                     null=True)
    back_rate = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='退款订单数占比',
                                    null=True)
    clickDeal2 = models.DecimalField(max_digits=10, decimal_places=4, verbose_name='成交转化率',
                                     null=True)
    GPM = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='GPM', null=True)

    class Meta:
        verbose_name = '直播间后台数据'
        verbose_name_plural = '直播间后台数据'
        db_table = 'taiwei_room'


class Integration(models.Model):
    code = models.CharField(max_length=50, verbose_name='款号', null=True)
    creation_date = models.DateField(verbose_name='创建日期', null=True)
    size = models.CharField(max_length=255, verbose_name='尺寸', null=True)
    season = models.CharField(max_length=20, verbose_name='季节', null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='成本', null=True)
    specification_sales = models.CharField(max_length=255, verbose_name='规格及销量', null=True)
    available_quantity = models.IntegerField(verbose_name='可卖量', null=True)
    stall_sales = models.IntegerField(verbose_name='档口销量', null=True)
    stall_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='档口价格', null=True)
    order_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单价格', null=True)
    category = models.CharField(max_length=50, verbose_name='品类', null=True)
    first_registration_time = models.DateField(verbose_name='初次到档口日期', null=True)
    last_registration_time = models.DateField(verbose_name='最后到档口日期', null=True)

    class Meta:
        verbose_name = '整合表'
        verbose_name_plural = '整合表'
        db_table = 'taiwei_Integration'


class ProductInformation(models.Model):
    code = models.CharField(max_length=255, verbose_name='款号', null=True)
    date = models.DateField(verbose_name='日期', null=True)
    exposure_count = models.IntegerField(verbose_name='曝光量', null=True)
    click_count = models.IntegerField(verbose_name='点击人数', null=True)
    total_exposure = models.IntegerField(verbose_name='总曝光次数', null=True)
    entry_count = models.IntegerField(verbose_name='进入次数', null=True)
    room_name = models.CharField(max_length=20, verbose_name="直播间名称", null=True)
    live_time = models.CharField(max_length=255, verbose_name="讲解时间", null=True)
    session = models.CharField(max_length=10, verbose_name="场次", null=True)
    click_rate = models.CharField(max_length=20, verbose_name="点击率", null=True)
    success_reta = models.CharField(max_length=20, verbose_name="成交率", null=True)
    in_live_rate = models.CharField(max_length=20, verbose_name="进入率", null=True)
    pay_combo_cnt = models.IntegerField(verbose_name="销量", null=True)

    class Meta:
        verbose_name = '商品讲解信息'
        verbose_name_plural = '商品讲解信息'
        db_table = "taiwei_product_info"
