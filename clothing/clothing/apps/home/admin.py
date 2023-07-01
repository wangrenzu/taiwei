from django.contrib import admin
from .models import Order, User, Goods, Materials, Commodity, Report, SalesRecord, Stock, OneCommodity


class OrderAdmin(admin.ModelAdmin):
    fieldsets = (
        ('订单信息', {
            'fields': ('order_no', 'sub_order_no', 'product_name', 'product_id', 'merchant_code')
        }),
        ('商品信息', {
            'fields': ('product_quantity', 'product_amount', 'order_total_amount')
        }),
        ('时间信息', {
            'fields': ('order_submit_time', 'payment_finish_time', 'order_finish_time')
        }),
        ('备注信息', {
            'fields': ('merchant_remark',)
        }),
        ('状态信息', {
            'fields': ('order_status', 'after_sale_status')
        }),
        ('地区信息', {
            'fields': ('province', 'city', 'district', 'street')
        }),
        ('达人信息', {
            'fields': ('influencer_id', 'influencer_nickname')
        }),
        ('广告信息', {
            'fields': ('ad_channel',)
        }),
    )

    list_display = (
        'sub_order_no', 'product_name', 'merchant_code', 'product_quantity', 'order_total_amount', 'order_submit_time',
        'order_finish_time',
    )
    list_filter = ('order_submit_time', 'order_finish_time', 'order_status', 'after_sale_status')
    search_fields = ('sub_order_no', 'merchant_code')


class UserAdmin(admin.ModelAdmin):
    list_display = ('sub_order_no', 'name', 'product_quantity', 'order_total_amount')
    search_fields = ('sub_order_no', 'name')
    list_filter = ('product_quantity',)


class GoodsAdmin(admin.ModelAdmin):
    list_display = ('merchant_code', 'merchant_name', 'price', 'merchant_english', 'category', 'season')
    search_fields = ('merchant_code',)
    list_filter = ('price',)


class MaterialsAdmin(admin.ModelAdmin):
    list_display = ('time', 'merchant_code', 'price', 'remark')
    search_fields = ('merchant_code',)
    list_filter = ('time', 'price')


class CommodityAdmin(admin.ModelAdmin):
    list_display = ('commodity_image', 'commodity_title', 'commodity_code', 'deal_amount', 'settlement_amount',
                    'deal_refund_amount', 'pre_shipment_refund_rate', 'post_shipment_refund_rate',
                    'live_exposure_count', 'live_click_count', 'live_deal_amount', 'live_deal_order_count',
                    'live_deal_item_count', 'live_deal_user_count', 'live_deal_conversion_rate')
    search_fields = ('commodity_title', 'commodity_code')


class OneCommodityAdmin(admin.ModelAdmin):
    list_display = ('commodity_title','live_deal_item_count', 'commodity_code', 'deal_amount', 'date_time')
    search_fields = ('commodity_title', 'commodity_code')
    list_filter = ('date_time',)
    ordering = ('-deal_amount',)


class ReportAdmin(admin.ModelAdmin):
    list_display = ('order_submit_time', 'wait_num', 'remove_num', 'transit_num', 'success_num', 'back_num')
    search_fields = ('order_submit_time',)
    list_filter = ('order_submit_time',)


class SalesRecordAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'product_code', 'product_name', 'specification', 'price', 'discount', 'quantity',
                    'total', 'barcode', 'store', 'transaction_time', 'outgoing_time')
    search_fields = ('recipient', 'product_code', 'store')
    list_filter = ('product_code',)


class StockAdmin(admin.ModelAdmin):
    list_display = ('house', 'code', 'inventory', 'order_quantity', 'waiting_quantity', 'orderable', 'shippable')
    search_fields = ('code', 'house')
    list_filter = ('house',)


admin.site.register(Order, OrderAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Goods, GoodsAdmin)
admin.site.register(Materials, MaterialsAdmin)
admin.site.register(Commodity, CommodityAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(SalesRecord, SalesRecordAdmin)
admin.site.register(OneCommodity, OneCommodityAdmin)
