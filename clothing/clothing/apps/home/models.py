from django.db import models


class Order(models.Model):
    order_no = models.CharField(max_length=100, verbose_name='主订单编号')
    sub_order_no = models.CharField(max_length=100, verbose_name='子订单编号', unique=True)
    product_name = models.CharField(max_length=100, verbose_name='选购商品')
    product_id = models.CharField(max_length=100, verbose_name='商品ID')
    merchant_code = models.CharField(max_length=100, verbose_name='商家编码')
    product_quantity = models.IntegerField(verbose_name='商品数量')
    product_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='商品金额')
    order_submit_time = models.DateTimeField(verbose_name='订单提交时间', null=True, blank=True)
    payment_finish_time = models.DateTimeField(verbose_name='支付完成时间', null=True, blank=True)
    order_finish_time = models.DateTimeField(verbose_name='订单完成时间', null=True, blank=True)
    merchant_remark = models.TextField(verbose_name='商家备注', null=True, blank=True)
    order_status = models.CharField(max_length=100, verbose_name='订单状态')
    after_sale_status = models.CharField(max_length=100, verbose_name='售后状态', null=True, blank=True)
    order_total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单应付金额')
    province = models.CharField(max_length=100, verbose_name='省')
    city = models.CharField(max_length=100, verbose_name='市')
    district = models.CharField(max_length=100, verbose_name='区')
    street = models.CharField(max_length=100, verbose_name='街道')
    influencer_id = models.CharField(max_length=100, verbose_name='达人ID', null=True, blank=True)
    influencer_nickname = models.CharField(max_length=100, verbose_name='达人昵称', null=True, blank=True)
    ad_channel = models.CharField(max_length=100, verbose_name='广告渠道', null=True, blank=True)

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'
        db_table = "taiwei_orders"


class User(models.Model):
    sub_order_no = models.CharField(max_length=100, verbose_name='子订单编号', unique=True)
    product_quantity = models.IntegerField(verbose_name='商品数量')
    name = models.CharField(max_length=30, verbose_name='名字')
    order_total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='订单应付金额')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        db_table = "taiwei_user"


class Goods(models.Model):
    merchant_code = models.CharField(max_length=100, verbose_name='货品编号', null=True)
    merchant_name = models.CharField(max_length=100, verbose_name='品名', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='固定成本价', null=True)
    create_time = models.DateTimeField(verbose_name='创建日期', null=True)
    merchant_english = models.CharField(max_length=200, verbose_name='英文名', null=True)
    category = models.CharField(max_length=10, verbose_name='品类', null=True)
    season = models.CharField(max_length=10, verbose_name='季节', null=True)

    class Meta:
        verbose_name = '货品信息'
        verbose_name_plural = '货品信息'
        db_table = "taiwei_goods"


class Stock(models.Model):
    house = models.CharField(max_length=30, verbose_name='仓库', null=True)
    code = models.CharField(max_length=10, verbose_name='货品编号', null=True)
    inventory = models.IntegerField(verbose_name='库存量')
    order_quantity = models.IntegerField(verbose_name='订购量')
    waiting_quantity = models.IntegerField(verbose_name='待发量')
    orderable = models.IntegerField(verbose_name='可订购')
    shippable = models.IntegerField(verbose_name='可发货')
    number = models.IntegerField(verbose_name='总销量', null=True)

    class Meta:
        verbose_name = '库存信息'
        verbose_name_plural = '库存信息'
        db_table = "taiwei_stock"


class new_Stock(models.Model):
    house = models.CharField(max_length=30, verbose_name='仓库', null=True)
    code = models.CharField(max_length=10, verbose_name='货品编号', null=True)
    cls = models.CharField(max_length=100, verbose_name='规格', null=True)
    inventory = models.IntegerField(verbose_name='库存量')
    order_quantity = models.IntegerField(verbose_name='订购量')
    waiting_quantity = models.IntegerField(verbose_name='待发量')
    orderable = models.IntegerField(verbose_name='可订购')
    shippable = models.IntegerField(verbose_name='可发货')

    class Meta:
        verbose_name = '新库存信息'
        verbose_name_plural = '新库存信息'
        db_table = "taiwei_newstock"


class Materials(models.Model):
    time = models.DateTimeField(verbose_name='日期', blank=True)
    merchant_code = models.CharField(max_length=100, verbose_name='款号', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额')
    remark = models.TextField(verbose_name='商家备注', null=True, blank=True)

    class Meta:
        verbose_name = '辅助材料购买'
        verbose_name_plural = '辅助材料购买'
        db_table = "taiwei_materials"


class Commodity(models.Model):
    commodity_image = models.CharField(max_length=200, verbose_name='商品图片', blank=True)
    commodity_title = models.CharField(max_length=100, verbose_name='商品标题', blank=True)
    commodity_code = models.CharField(max_length=100, verbose_name='商品编号', blank=True)
    deal_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='成交金额', blank=True)
    settlement_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='实际结算金额', blank=True)
    deal_refund_amount = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='成交退款率', blank=True)
    pre_shipment_refund_rate = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='发货前成交退款率',
                                                   blank=True)
    post_shipment_refund_rate = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='发货后成交退款率',
                                                    blank=True)
    live_exposure_count = models.IntegerField(verbose_name='直播间商品曝光人数', blank=True)
    live_click_count = models.IntegerField(verbose_name='直播间商品点击人数', blank=True)
    live_deal_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='直播间成交金额', blank=True)
    live_deal_order_count = models.IntegerField(verbose_name='直播间成交订单数', blank=True)
    live_deal_item_count = models.IntegerField(verbose_name='直播间成交件数', blank=True)
    live_deal_user_count = models.IntegerField(verbose_name='直播间成交人数', blank=True)
    live_deal_conversion_rate = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='直播间成交转化率',
                                                    blank=True)
    quality_return_rate = models.FloatField(verbose_name='品质退货率', null=True)  # 品质退货率
    negative_review_rate = models.FloatField(verbose_name='差评率', null=True)  # 差评率
    positive_review_count = models.IntegerField(verbose_name='好评数', null=True)  # 好评数

    class Meta:
        verbose_name = '30天全量商品表'
        verbose_name_plural = '30天全量商品表'
        db_table = "taiwei_commodity"


class Report(models.Model):
    order_submit_time = models.DateField(verbose_name='日期', null=True)
    wait_num = models.IntegerField(verbose_name='代发', null=True)
    remove_num = models.IntegerField(verbose_name='取消', null=True)
    transit_num = models.IntegerField(verbose_name='在途', null=True)
    success_num = models.IntegerField(verbose_name='成功', null=True)
    back_num = models.IntegerField(verbose_name='退回', null=True)
    data_time = models.DateField(verbose_name="上传日期", null=True)

    class Meta:
        verbose_name = '每日报表'
        verbose_name_plural = '每日报表'
        db_table = "taiwei_report"


class SalesRecord(models.Model):
    recipient = models.CharField(verbose_name="收货人", max_length=100, null=True)
    product_code = models.CharField(verbose_name="货品编号", max_length=100, null=True)
    product_name = models.CharField(verbose_name="品名", max_length=100, null=True)
    specification = models.CharField(verbose_name="规格", max_length=100, null=True)
    price = models.DecimalField(verbose_name="价格", max_digits=10, decimal_places=2, null=True)
    discount = models.DecimalField(verbose_name="折扣", max_digits=5, decimal_places=2, null=True)
    quantity = models.IntegerField(verbose_name="数量", null=True)
    total = models.DecimalField(verbose_name="合计", max_digits=10, decimal_places=2, null=True)
    barcode = models.CharField(verbose_name="条码", max_length=100, null=True)
    store = models.CharField(verbose_name="店铺", max_length=100, null=True)
    transaction_time = models.DateTimeField(verbose_name="交易时间", null=True)
    outgoing_time = models.DateTimeField(verbose_name="出库时间", null=True)

    class Meta:
        verbose_name = '档口销量'
        verbose_name_plural = '档口销量'
        db_table = "taiwei_salesrecord"


class StockIn(models.Model):
    product_code = models.CharField(max_length=100, verbose_name='货品货号')
    product_name = models.CharField(max_length=100, verbose_name='货品名称')
    specification = models.CharField(max_length=100, verbose_name='规格')
    quantity = models.IntegerField(verbose_name='数量')
    reason = models.CharField(max_length=100, verbose_name='入库原因')
    handler = models.CharField(max_length=100, verbose_name='经办人')
    registration_time = models.DateTimeField(verbose_name='登记时间')

    class Meta:
        verbose_name = '入库'
        verbose_name_plural = '入库信息'
        db_table = 'taiwei_stock_in'


class OrderTracking(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='款号')
    name = models.CharField(max_length=100, null=True, verbose_name='货品名称')
    image = models.CharField(max_length=200, blank=True, null=True, verbose_name='图片')
    order_quantity = models.IntegerField(blank=True, null=True, verbose_name='订购量')
    cutting_quantity = models.IntegerField(blank=True, null=True, verbose_name='裁床仓')
    workshop_quantity = models.IntegerField(blank=True, null=True, verbose_name='车间')
    rear_quantity = models.IntegerField(blank=True, null=True, verbose_name='后道')
    taiwei_quantity = models.IntegerField(blank=True, null=True, verbose_name='泰维')
    yifa_quantity = models.IntegerField(blank=True, null=True, verbose_name='意法')
    moya_quantity = models.IntegerField(blank=True, null=True, verbose_name='茉雅')
    live_exposure_count = models.IntegerField(blank=True, null=True, verbose_name='直播间曝光')
    live_deal_item_count = models.IntegerField(blank=True, null=True, verbose_name='成交件数')
    cancelled_quantity = models.IntegerField(blank=True, null=True, verbose_name='取消')
    pending_shipment_quantity = models.IntegerField(blank=True, null=True, verbose_name='待发+在途')
    successful_quantity = models.IntegerField(blank=True, null=True, verbose_name='成功')
    returned_quantity = models.IntegerField(blank=True, null=True, verbose_name='退回')

    class Meta:
        verbose_name = '订单跟踪'
        verbose_name_plural = '订单跟踪'
        db_table = 'taiwei_tracking'


class OneCommodity(models.Model):
    commodity_image = models.CharField(max_length=200, verbose_name='商品图片', blank=True)
    commodity_title = models.CharField(max_length=100, verbose_name='商品标题', blank=True)
    commodity_code = models.CharField(max_length=100, verbose_name='商品编号', blank=True)
    deal_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='成交金额', blank=True)
    settlement_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='实际结算金额', blank=True)
    deal_refund_amount = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='成交退款率', blank=True)
    pre_shipment_refund_rate = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='发货前成交退款率',
                                                   blank=True)
    post_shipment_refund_rate = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='发货后成交退款率',
                                                    blank=True)
    live_exposure_count = models.IntegerField(verbose_name='直播间商品曝光人数', blank=True)
    live_click_count = models.IntegerField(verbose_name='直播间商品点击人数', blank=True)
    live_deal_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='直播间成交金额', blank=True)
    live_deal_order_count = models.IntegerField(verbose_name='直播间成交订单数', blank=True)
    live_deal_item_count = models.IntegerField(verbose_name='直播间成交件数', blank=True)
    live_deal_user_count = models.IntegerField(verbose_name='直播间成交人数', blank=True)
    live_deal_conversion_rate = models.DecimalField(max_digits=10, decimal_places=6, verbose_name='直播间成交转化率',
                                                    blank=True)
    date_time = models.DateField(verbose_name='日期')

    class Meta:
        verbose_name = '每天全量商品表'
        verbose_name_plural = '每天全量商品表'
        db_table = "taiwei_onecommodity"


class UpdateStatus(models.Model):
    name = models.CharField(max_length=30, verbose_name='名称', unique=True)
    date_time = models.CharField(max_length=10, verbose_name='最后提交时间', null=True)

    class Meta:
        verbose_name = '最后上传时间'
        verbose_name_plural = '最后上传时间'
        db_table = "taiwei_updatestatus"


class VipUser(models.Model):
    name = models.CharField(max_length=100, verbose_name="昵称", unique=True)

    class Meta:
        verbose_name = 'VIP用户'
        verbose_name_plural = 'VIP用户'
        db_table = "taiwei_vipuser"


class Size(models.Model):
    code = models.CharField(max_length=30, verbose_name='款号')
    size = models.CharField(max_length=200, verbose_name='尺寸')

    class Meta:
        verbose_name = '尺寸'
        verbose_name_plural = '尺寸'
        db_table = "taiwei_size"


class newStyle(models.Model):
    date = models.DateField(verbose_name='日期', null=True)
    code = models.CharField(max_length=200, verbose_name='款号', null=True)
    designer = models.CharField(max_length=200, verbose_name='设计师', null=True)
    number_of_pieces = models.CharField(max_length=200, verbose_name='件数', null=True)
    total_number_of_pieces = models.IntegerField(verbose_name='总件数', null=True)
    order_maker = models.DateField(max_length=200, verbose_name='做下单表', null=True)
    confirmation_on_the_day = models.CharField(max_length=200, verbose_name='当天确认', null=True)
    fabric_arrival_time = models.DateField(verbose_name='面料到库时间', null=True)
    circulation_table_flow_down_time = models.DateField(verbose_name='流转表流下时间', null=True)
    material_fill_craft_package_material_post_road = models.DecimalField(max_digits=10, decimal_places=2,
                                                                         verbose_name='面辅料+充绒+工艺+包材+后道',
                                                                         null=True)
    category = models.CharField(max_length=200, verbose_name='类目', null=True)

    class Meta:
        verbose_name = '下单简报'
        verbose_name_plural = '下单简报'
        db_table = "taiwei_new_style"


class repeatOrder(models.Model):
    date = models.DateField(verbose_name='日期', null=True)
    code = models.CharField(max_length=200, verbose_name='款号', null=True)
    number_of_pieces = models.CharField(max_length=255, verbose_name='件数', null=True)
    total_number_of_pieces = models.IntegerField(verbose_name='总件数', null=True)
    circulation = models.DateField(verbose_name='做流转表', null=True)
    daily_status = models.CharField(max_length=200, verbose_name='当日状况', null=True)
    fabric_arrival_time = models.DateField(verbose_name='面料到库时间', null=True)
    circulation_table_flow_down = models.DateField(verbose_name='流转表流下', null=True)

    class Meta:
        verbose_name = '翻单'
        verbose_name_plural = '翻单'
        db_table = "taiwei_repeat_order"


class Fabric(models.Model):
    time = models.DateField(verbose_name='日期', blank=True)
    merchant_code = models.CharField(max_length=100, verbose_name='款号', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='金额', null=True)
    channel = models.CharField(max_length=100, verbose_name='渠道', null=True, blank=True)
    role = models.CharField(max_length=2000, verbose_name='用途', null=True, blank=True)

    class Meta:
        verbose_name = '面料表'
        verbose_name_plural = '面料表'
        db_table = "taiwei_fabric"


class Factory(models.Model):
    code = models.CharField(max_length=100, verbose_name='款号', null=True)
    date = models.DateField(verbose_name='日期', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='总金额', null=True)
    num = models.FloatField(verbose_name='件数', null=True)
    factory = models.CharField(max_length=30, verbose_name='工厂', null=True, blank=True)
    file_name = models.CharField(max_length=30, verbose_name='文件名', null=True, blank=True)

    class Meta:
        verbose_name = '工厂表'
        verbose_name_plural = '工厂表'
        db_table = "taiwei_factory"


class StyleStatus(models.Model):
    time = models.DateField(verbose_name="简报日期", null=True)
    date_time = models.DateField(verbose_name="上传日期", null=True)
    code = models.CharField(verbose_name="款号", max_length=30, null=True)
    cai_chuang = models.IntegerField(verbose_name="裁床", null=True)
    che_jian = models.IntegerField(verbose_name="车间", null=True)
    hou_dao = models.IntegerField(verbose_name="后道", null=True)
    tai_wei = models.IntegerField(verbose_name="泰维", null=True)
    yi_fa = models.IntegerField(verbose_name="意法", null=True)
    mo_ya = models.IntegerField(verbose_name="茉雅", null=True)
    fabric_price = models.FloatField(verbose_name="面料金额", null=True)
    materials_price = models.FloatField(verbose_name="辅料金额", null=True)
    factory_price = models.FloatField(verbose_name="工厂金额", null=True)
    salesrecord_price = models.FloatField(verbose_name="档口金额", null=True)
    order_price = models.FloatField(verbose_name="订单金额", null=True)
    to_salesrecord_time = models.DateField(verbose_name="最近到档口时间", null=True)
    time_num = models.IntegerField(verbose_name="下单到今天天数", null=True)
    tags = models.CharField(verbose_name="标签", max_length=255, null=True)
    remarks = models.TextField(verbose_name="备注", null=True)
    is_other = models.BooleanField(verbose_name="是否是其他", default=False)
    num = models.IntegerField(verbose_name="来几次", null=True)

    class Meta:
        verbose_name = '新款状态'
        verbose_name_plural = '新款状态'
        db_table = 'taiwei_style_status'
