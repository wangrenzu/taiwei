from datetime import datetime

from rest_framework import serializers
from .models import Order, User, Report, StockIn, OrderTracking, Stock, UpdateStatus, VipUser, StyleStatus, \
    NewStyleStatusTracking, Goods


class OrderSerializer(serializers.ModelSerializer):
    merchant_code_prefix = serializers.CharField(allow_blank=True, required=False)
    order_count = serializers.CharField(allow_blank=True, required=False)

    class Meta:
        model = Order
        fields = '__all__'


class StockInSerializer(serializers.ModelSerializer):
    first_registration_time = serializers.DateField()
    inventory = serializers.IntegerField()
    last_registration_time = serializers.DateField()
    count_quantity = serializers.IntegerField()

    class Meta:
        model = StockIn
        fields = ('product_code', 'product_name', 'inventory', 'count_quantity', 'quantity', 'first_registration_time',
                  'last_registration_time')


class StockInSerializer2(serializers.ModelSerializer):
    id = serializers.IntegerField()
    product_name = serializers.CharField()
    inventory = serializers.IntegerField()
    count_quantity = serializers.IntegerField()
    quantity = serializers.IntegerField()
    first_registration_time = serializers.DateField()
    last_registration_time = serializers.DateField()

    class Meta:
        model = StockIn
        fields = ('id', 'product_code', 'product_name', 'inventory', 'count_quantity',
                  'quantity', 'first_registration_time',
                  'last_registration_time')


class StockInSerializer3(serializers.ModelSerializer):
    code = serializers.CharField()
    category = serializers.CharField()
    price = serializers.IntegerField()
    commodity_image = serializers.CharField()
    live_deal_item_count = serializers.IntegerField()
    live_deal_conversion_rate = serializers.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        model = Stock
        fields = ('id', 'code', 'category', 'price', 'commodity_image', 'inventory',
                  'order_quantity', 'live_deal_item_count', 'live_deal_conversion_rate')


class StockInSerializer12(serializers.ModelSerializer):
    code = serializers.CharField()
    category = serializers.CharField()
    price = serializers.IntegerField()
    commodity_image = serializers.CharField()
    live_deal_item_count = serializers.IntegerField()
    live_deal_conversion_rate = serializers.DecimalField(max_digits=10, decimal_places=4)
    date_time = serializers.DateField()

    class Meta:
        model = Stock
        fields = ('id', 'code', 'category', 'price', 'commodity_image', 'inventory',
                  'order_quantity', 'live_deal_item_count', 'live_deal_conversion_rate',
                  'date_time')


class OrderSearchSerializer(serializers.ModelSerializer):
    merchant_code_prefix = serializers.CharField()
    order_count = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ('merchant_code_prefix', 'order_count')


class UserOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class StyleStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StyleStatus
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    total_quantity = serializers.IntegerField()
    name = serializers.CharField()
    total_amount = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('total_quantity', 'name', 'total_amount')


class Search3Result:
    def __init__(self, id, m, sum_total_amount_3, sum_product_quantity_3, sum_total_amount_5, sum_product_quantity_5,
                 pending_and_in_transit, pending_and_in_transit_num, returned, returned_num, inventory,
                 commodity_image):
        self.id = id
        self.m = m
        self.sum_total_amount_3 = sum_total_amount_3
        self.sum_product_quantity_3 = sum_product_quantity_3
        self.sum_total_amount_5 = sum_total_amount_5
        self.sum_product_quantity_5 = sum_product_quantity_5
        self.pending_and_in_transit = pending_and_in_transit
        self.pending_and_in_transit_num = pending_and_in_transit_num
        self.returned = returned
        self.returned_num = returned_num
        self.inventory = inventory
        self.commodity_image = commodity_image


class Search3Order(serializers.Serializer):
    id = serializers.IntegerField()
    sum_total_amount_3 = serializers.IntegerField()
    sum_product_quantity_3 = serializers.IntegerField()
    sum_total_amount_5 = serializers.IntegerField()
    sum_product_quantity_5 = serializers.IntegerField()
    m = serializers.CharField()
    pending_and_in_transit = serializers.DecimalField(max_digits=10, decimal_places=2)
    pending_and_in_transit_num = serializers.IntegerField()
    returned = serializers.DecimalField(max_digits=10, decimal_places=2)
    returned_num = serializers.IntegerField()
    inventory = serializers.IntegerField()
    commodity_image = serializers.CharField()

    class Meta:
        model = Search3Result
        fields = (
            'id', 'sum_total_amount_3', 'm', 'sum_product_quantity_3', 'sum_total_amount_5', 'sum_product_quantity_5',
            'pending_and_in_transit', 'pending_and_in_transit_num', 'returned', 'returned_num', 'inventory',
            'commodity_image')


class Search4Result:
    def __init__(self, id, name, first_day, recently_day, sum_orders, success_money, back_money, wait_money,
                 transit_money, back_rate, success_num, back_num, wait_num, transit_num, success_rate, real_rate,
                 not_day, new_user, sum_score):
        self.id = id
        self.name = name
        self.first_day = first_day
        self.recently_day = recently_day
        self.sum_orders = sum_orders
        self.success_money = success_money
        self.back_money = back_money
        self.wait_money = wait_money
        self.transit_money = transit_money
        self.back_rate = back_rate
        self.success_num = success_num
        self.back_num = back_num
        self.wait_num = wait_num
        self.transit_num = transit_num
        self.success_rate = success_rate
        self.real_rate = real_rate
        self.not_day = not_day
        self.new_user = new_user
        self.sum_score = sum_score


class Search4Order(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    first_day = serializers.DateField()
    recently_day = serializers.DateField()
    sum_orders = serializers.IntegerField()
    success_money = serializers.IntegerField()
    back_money = serializers.IntegerField()
    wait_money = serializers.IntegerField()
    transit_money = serializers.IntegerField()
    back_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    success_num = serializers.IntegerField()
    back_num = serializers.IntegerField()
    wait_num = serializers.IntegerField()
    transit_num = serializers.IntegerField()
    success_rate = serializers.IntegerField()
    real_rate = serializers.IntegerField()
    not_day = serializers.IntegerField()
    new_user = serializers.CharField()
    sum_score = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Search4Result
        fields = (
            'id', 'name', 'first_day', 'recently_day', 'sum_orders', 'success_money', 'back_money', 'wait_money',
            'transit_money', 'back_rate', 'success_num', 'back_num', 'wait_num', 'transit_num', 'success_rate',
            'real_rate', 'not_day', 'new_user', 'sum_score'
        )


class Search5Result:
    def __init__(self, id, name, first_day, recently_day, sum_orders, success_money, back_money, wait_money,
                 transit_money, run_single, category, back_rate, success_num, back_num, wait_num, transit_num,
                 success_rate, real_rate, not_day, inventory):
        self.id = id
        self.name = name
        self.first_day = first_day
        self.recently_day = recently_day
        self.sum_orders = sum_orders
        self.success_money = success_money
        self.back_money = back_money
        self.wait_money = wait_money
        self.transit_money = transit_money
        self.run_single = run_single
        self.category = category
        self.back_rate = back_rate
        self.success_num = success_num
        self.back_num = back_num
        self.wait_num = wait_num
        self.transit_num = transit_num
        self.success_rate = success_rate
        self.real_rate = real_rate
        self.not_day = not_day
        self.inventory = inventory


class Search5Order(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    first_day = serializers.DateField()
    recently_day = serializers.DateField()
    sum_orders = serializers.IntegerField()
    success_money = serializers.DecimalField(max_digits=10, decimal_places=2)
    back_money = serializers.DecimalField(max_digits=10, decimal_places=2)
    wait_money = serializers.DecimalField(max_digits=10, decimal_places=2)
    transit_money = serializers.DecimalField(max_digits=10, decimal_places=2)
    run_single = serializers.IntegerField()
    category = serializers.CharField()
    back_rate = serializers.DecimalField(max_digits=5, decimal_places=2)
    success_num = serializers.IntegerField()
    back_num = serializers.IntegerField()
    wait_num = serializers.IntegerField()
    transit_num = serializers.IntegerField()
    success_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    real_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    not_day = serializers.IntegerField()
    inventory = serializers.IntegerField()

    class Meta:
        model = Search5Result
        fields = (
            'id', 'name', 'first_day', 'recently_day', 'sum_orders', 'success_money', 'back_money', 'wait_money',
            'transit_money', 'run_single', 'category', 'back_rate', 'success_num', 'back_num', 'wait_num',
            'transit_num', 'success_rate', 'real_rate', 'not_day', 'inventory')


class UserInfoSerializer(serializers.ModelSerializer):
    commodity_image = serializers.CharField()
    merchant_code = serializers.CharField()
    product_name = serializers.CharField()
    category = serializers.CharField()
    price = serializers.IntegerField()

    class Meta:
        model = User
        fields = ('name', 'commodity_image', 'merchant_code', 'product_name', 'category', 'price')


class CodeInfoSerializer(serializers.ModelSerializer):
    code = serializers.CharField()
    commodity_image = serializers.CharField()
    category = serializers.CharField()
    product_quantity = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ('code', 'commodity_image', 'category', 'product_quantity')


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'


class Search6Result:
    def __init__(self, id, code, category, stock, cost, sales, first_registration_time,
                 last_registration_time, number, create_time, season):
        self.id = id
        self.code = code
        self.category = category
        self.stock = stock
        self.cost = cost
        self.sales = sales
        self.first_registration_time = first_registration_time
        self.last_registration_time = last_registration_time
        self.number = number
        self.create_time = create_time
        self.season = season


class Search6Order(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField()
    category = serializers.CharField()
    stock = serializers.IntegerField()
    cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    sales = serializers.IntegerField()
    first_registration_time = serializers.DateField()
    last_registration_time = serializers.DateField()
    number = serializers.IntegerField()
    create_time = serializers.DateField()
    season = serializers.CharField()

    class Meta:
        model = Search6Result
        fields = (
            'id', 'code', 'category', 'stock', 'cost', 'sales', 'first_registration_time', 'last_registration_time',
            'number', 'create_time', 'season')


class OrderTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderTracking
        fields = '__all__'


class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpdateStatus
        fields = '__all__'


class VipUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = VipUser
        fields = ('name',)


class Search10Result:
    def __init__(self, id, merchant_code, category, date_time, live_exposure_count, one_live_deal_item_count, quantity,
                 first_time, last_time, inventory, live_deal_item_count, create_time, season):
        self.id = id
        self.merchant_code = merchant_code
        self.category = category
        self.date_time = date_time
        self.live_exposure_count = live_exposure_count
        self.one_live_deal_item_count = one_live_deal_item_count
        self.quantity = quantity
        self.first_time = first_time
        self.last_time = last_time
        self.inventory = inventory
        self.live_deal_item_count = live_deal_item_count
        self.create_time = create_time
        self.season = season


class Search10Order(serializers.Serializer):
    id = serializers.IntegerField()
    merchant_code = serializers.CharField()
    category = serializers.CharField()
    date_time = serializers.DateField()
    live_exposure_count = serializers.IntegerField()
    one_live_deal_item_count = serializers.IntegerField()
    quantity = serializers.IntegerField()
    first_time = serializers.DateField()
    last_time = serializers.DateField()
    inventory = serializers.IntegerField()
    live_deal_item_count = serializers.IntegerField()
    create_time = serializers.DateField()
    season = serializers.CharField()

    class Meta:
        model = Search10Result
        fields = (
            'id', 'merchant_code', 'category', 'date_time', 'live_exposure_count', 'one_live_deal_item_count',
            'quantity', 'first_time', 'last_time', 'inventory', 'live_deal_item_count',
            'create_time', 'season')


class Search11Result:
    def __init__(self, id, code, category, commodity_image, inventory, order_quantity, price,
                 live_deal_item_count, pre_shipment_refund_rate, post_shipment_refund_rate,
                 order_submit_time, one_live_exposure_count, one_live_deal_item_count,
                 quantity, first_registration_time, last_registration_time):
        self.id = id
        self.code = code
        self.category = category
        self.commodity_image = commodity_image
        self.inventory = inventory
        self.order_quantity = order_quantity
        self.price = price
        self.live_deal_item_count = live_deal_item_count
        self.pre_shipment_refund_rate = pre_shipment_refund_rate
        self.post_shipment_refund_rate = post_shipment_refund_rate
        self.order_submit_time = datetime.strptime(str(order_submit_time), "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
        self.one_live_exposure_count = one_live_exposure_count
        self.one_live_deal_item_count = one_live_deal_item_count
        self.quantity = quantity
        self.first_registration_time = first_registration_time
        self.last_registration_time = last_registration_time


class Search11Order(serializers.Serializer):
    id = serializers.IntegerField()
    code = serializers.CharField()
    category = serializers.CharField()
    commodity_image = serializers.CharField()
    inventory = serializers.IntegerField()
    order_quantity = serializers.IntegerField()
    price = serializers.IntegerField()
    live_deal_item_count = serializers.IntegerField()
    pre_shipment_refund_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    post_shipment_refund_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    order_submit_time = serializers.DateField()
    one_live_exposure_count = serializers.IntegerField()
    one_live_deal_item_count = serializers.IntegerField()
    quantity = serializers.IntegerField()
    first_registration_time = serializers.DateField()
    last_registration_time = serializers.DateField()

    class Meta:
        model = Search10Result
        fields = (
            'id', 'code', 'category', 'commodity_image', 'inventory',
            'order_quantity', 'price', 'live_deal_item_count', 'pre_shipment_refund_rate',
            'post_shipment_refund_rate', 'order_submit_time', 'one_live_exposure_count',
            'one_live_deal_item_count', 'quantity', 'first_registration_time', 'last_registration_time')


class NewStyleStatusTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewStyleStatusTracking
        fields = '__all__'


class GoodsSerializer(serializers.ModelSerializer):
    code = serializers.CharField()
    inventory = serializers.IntegerField()

    class Meta:
        model = Goods
        fields = ("code", "category", "inventory")


class StyleStatusNumSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    num = serializers.IntegerField()

    class Meta:
        model = NewStyleStatusTracking
        fields = ("label", "category", "total_quantity", "num")
