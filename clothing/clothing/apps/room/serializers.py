from rest_framework import serializers
from .models import Room, Integration


class RoomSerializer(serializers.ModelSerializer):
    back_num = serializers.IntegerField()
    pending_and_in_transit_num = serializers.IntegerField()
    cart_exposure = serializers.IntegerField()
    cart_clickExposure = serializers.DecimalField(max_digits=10, decimal_places=4)
    cart_clickDeal = serializers.DecimalField(max_digits=10, decimal_places=4)
    cart_salesPrice = serializers.IntegerField()
    cart_salesNum = serializers.IntegerField()
    prev_order_number = serializers.IntegerField()
    prev_order_rate = serializers.DecimalField(max_digits=10, decimal_places=4)
    prev_back_rate = serializers.DecimalField(max_digits=10, decimal_places=4)
    prev_clickDeal2 = serializers.DecimalField(max_digits=10, decimal_places=4)
    prev_GPM = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Room
        fields = ('id', 'product_id', 'code', 'img', 'characteristic', 'back_num', 'pending_and_in_transit_num',
                  'exposure', 'clickExposure', 'clickDeal', 'salesPrice', 'salesNum', 'cart_exposure',
                  'cart_clickExposure', 'cart_clickDeal', 'cart_salesPrice', 'cart_salesNum',
                  'order_number', 'order_rate', 'back_rate', 'clickDeal2', 'GPM', 'prev_order_number',
                  'prev_order_rate', 'prev_back_rate', 'prev_clickDeal2', 'prev_GPM')


class IntegrationSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    img = serializers.CharField()
    r_code = serializers.CharField()

    class Meta:
        model = Integration
        fields = ('code', 'product_id', 'img', 'creation_date', 'size', 'season',
                  'cost', 'specification_sales', 'available_quantity', 'stall_sales',
                  'stall_price', 'order_price', 'category', 'r_code', 'first_registration_time',
                  'last_registration_time')
