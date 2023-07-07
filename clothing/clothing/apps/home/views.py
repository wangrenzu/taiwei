import io
from django.db.models import Q, OuterRef, Subquery
from django.db.models import Max
import pandas as pd
from django.db import DatabaseError, connection
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

import msoffcrypto
from .models import Order, User, Goods, Materials, Commodity, Stock, Report, SalesRecord, new_Stock, StockIn, \
    OrderTracking, OneCommodity, UpdateStatus, VipUser, Size, newStyle, repeatOrder, Fabric, Factory, StyleStatus, \
    NewStyleStatusTracking
from .paginations import OrderPagination
from .serializers import OrderSerializer, UserOrderSerializer, \
    Search3Order, Search3Result, Search4Order, Search4Result, UserInfoSerializer, Search5Order, Search5Result, \
    ReportSerializer, CodeInfoSerializer, Search6Order, Search6Result, StockInSerializer, StockInSerializer2, \
    OrderTrackingSerializer, StockInSerializer3, UpdateStatusSerializer, VipUserSerializer, Search10Order, \
    Search10Result, Search11Order, Search11Result, StockInSerializer12, StyleStatusSerializer, \
    NewStyleStatusTrackingSerializer
from datetime import datetime, timedelta
from django.db import transaction
import logging

from room.models import Integration

logger = logging.getLogger(__name__)


# 带分页的订单数据
class HomeAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    pagination_class = OrderPagination
    ordering = ['product_quantity']


# 不带分页的订单数据
class HomeAllView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    ordering = ['product_quantity']


# 上传更新订单数据
class UpdateOrder(APIView):
    def post(self, request):
        excel_file = request.data.get('excel-file')
        if not excel_file:
            return Response({'error': '文件未上传'}, status=400)

            # 处理Excel文件，提取数据或存储到数据库
        df = pd.read_excel(excel_file, header=0)
        sub_order_nos = [row['子订单编号'] for index, row in df.iterrows()]

        orders = insert(df)
        query = '''
                    INSERT INTO taiwei_report (order_submit_time, wait_num, remove_num, transit_num, success_num, back_num, data_time)
                    SELECT
                    MAX(submit_time) as order_submit_time,
                    MAX(wait_num) as wait_num,
                    MAX(remove_num) as remove_num,
                    MAX(transit_num) as transit_num,
                    MAX(success_num) as success_num,
                    MAX(back_num) as back_num,
                    CURDATE() as data_time
                    FROM(
                    SELECT CAST(order_submit_time AS DATE) as submit_time,
                    SUM(product_quantity) as wait_num ,
                    NULL as remove_num,
                    NULL as transit_num,
                    NULL as success_num,
                    NULL as back_num
                    FROM taiwei_orders
                    WHERE 
                    (order_status = '待发货' AND after_sale_status = '-')
                    AND order_submit_time >= CURDATE() - INTERVAL 30 DAY
                    GROUP BY CAST(order_submit_time AS DATE)

                    UNION ALL

                    SELECT CAST(order_submit_time AS DATE) as submit_time,
                    NULL as wait_num,
                    SUM(product_quantity) as remove_num,
                    NULL as transit_num,
                    NULL as success_num,
                    NULL as back_num 
                    FROM taiwei_orders
                    WHERE 
                    (order_status = '已关闭' AND (after_sale_status like '%%退款成功%%' AND (merchant_remark LIKE '%%取消%%' OR merchant_remark='nan')))
                    AND order_submit_time >= CURDATE() - INTERVAL 30 DAY
                    GROUP BY CAST(order_submit_time AS DATE)

                    UNION ALL

                    SELECT CAST(order_submit_time AS DATE) as submit_time,
                    NULL as wait_num,
                    NULL as remove_num,
                    SUM(product_quantity) as transit_num,
                    NULL as success_num,
                    NULL as back_num  
                    FROM taiwei_orders
                    WHERE 
                    (order_status = '已发货' AND (after_sale_status LIKE '%%售后关闭%%' OR after_sale_status = '-'))
                    AND order_submit_time >= CURDATE() - INTERVAL 30 DAY
                    GROUP BY CAST(order_submit_time AS DATE)


                    UNION ALL

                    SELECT CAST(order_submit_time AS DATE) as submit_time,
                    NULL as wait_num,
                    NULL as remove_num,
                    NULL as transit_num,
                    SUM(product_quantity) as success_num,
                    NULL as back_num  
                    FROM taiwei_orders
                    WHERE 
                    (order_status = '已完成' AND (after_sale_status LIKE '%%售后关闭%%' OR after_sale_status = '-'))
                    AND order_submit_time >= CURDATE() - INTERVAL 30 DAY
                    GROUP BY CAST(order_submit_time AS DATE)


                    UNION ALL


                    SELECT CAST(order_submit_time AS DATE) as submit_time,
                    NULL as wait_num,
                    NULL as remove_num,
                    NULL as success_num,
                    NULL as transit_num,
                  SUM(product_quantity) as back_num		
                    FROM taiwei_orders
                    WHERE 
                    ((order_status = '已关闭' AND (after_sale_status LIKE '%%退款成功%%' 
                    AND (merchant_remark LIKE '%%退货%'
                     OR merchant_remark LIKE '%%拒收%%'
                     OR merchant_remark LIKE '%%退回%%')))
                    OR (order_status = '已发货' AND 
                    (after_sale_status LIKE '%%售后待处理%%' 
                    OR after_sale_status LIKE '%%待收退货%%' 
                    OR after_sale_status LIKE '%%待退货%%' 
                    OR after_sale_status LIKE '%%退款成功%%' ))
                    OR (order_status='已完成' AND 
                    (after_sale_status LIKE '%待收退货%' 
                    OR after_sale_status LIKE '%待退货%' 
                    OR after_sale_status LIKE '%退款成功%')))
                    AND order_submit_time >= CURDATE() - INTERVAL 30 DAY
                    GROUP BY CAST(order_submit_time AS DATE)
                    )as table1
                     GROUP BY submit_time
        '''

        try:

            with transaction.atomic():
                # 插入订单数据
                Order.objects.filter(sub_order_no__in=sub_order_nos).delete()
                inserted_count = Order.objects.bulk_create(orders)

            # 确保订单数据插入成功后再执行查询
            if inserted_count:
                with transaction.atomic():
                    # 执行查询语句
                    Report.objects.filter(data_time=datetime.now().strftime("%Y-%m-%d")).delete()
                    cursor = connection.cursor()
                    cursor.execute(query)

            # 提交事务
            return JsonResponse({'message': f'{len(inserted_count)} 条数据更新成功。'})
        except DatabaseError as e:
            return JsonResponse({'error': str(e)}, status=500)


# 添加订单数据
def insert(df):
    orders = []
    for index, row in df.iterrows():
        row['订单提交时间'] = str(row['订单提交时间'])
        if row['订单提交时间'] == "nan":
            order_submit_time = None
        else:
            dt = datetime.strptime(row['订单提交时间'].strip(), '%Y-%m-%d %H:%M:%S')
            order_submit_time = dt
        row['支付完成时间'] = str(row['支付完成时间'])
        if row['支付完成时间'] == "nan":
            payment_finish_time = None
        else:
            dt = datetime.strptime(row['支付完成时间'].strip(), '%Y-%m-%d %H:%M:%S')
            payment_finish_time = dt
        row['订单完成时间'] = str(row['订单完成时间'])
        if row['订单完成时间'] == "nan":
            order_finish_time = None
        else:
            dt = datetime.strptime(row['订单完成时间'].strip(), '%Y-%m-%d %H:%M:%S')
            order_finish_time = dt
        if len(str(row['商家编码'])) < 4:
            if "样衣" in str(row['选购商品']):
                row['商家编码'] = '样衣'
            else:
                row['商家编码'] = '微瑕'
        order = Order(
            order_no=str(row['主订单编号']).strip(),
            sub_order_no=str(row['子订单编号']).strip(),
            product_name=row['选购商品'],
            product_id=row['商品ID'],
            merchant_code=row['商家编码'].strip(),
            product_quantity=row['商品数量'],
            product_amount=row['商品金额'],
            order_submit_time=order_submit_time,
            payment_finish_time=payment_finish_time,
            order_finish_time=order_finish_time,
            merchant_remark=row['商家备注'],
            order_status=row['订单状态'],
            after_sale_status=row['售后状态'],
            order_total_amount=row['订单应付金额'],
            province=row['省'],
            city=row['市'],
            district=row['区'],
            street=row['街道'],
            influencer_id=row['达人ID'],
            influencer_nickname=row['达人昵称'],
            ad_channel=row['广告渠道']
        )
        orders.append(order)
    return orders


# 上传更新用户数据
class UpdateUser(APIView):
    def post(self, request):
        excel_file = request.data.get('excel-file')
        if not excel_file:
            return Response({'error': '文件未上传'}, status=400)

            # 处理Excel文件，提取数据或存储到数据库
        df = pd.read_excel(excel_file, header=0)
        user_list = []
        sub_order_nos = [row.iloc[1].strip().split(";") for index, row in df.iterrows() if
                         len(row.iloc[1].strip()) > 20]
        sub_order_nos = [item for sublist in sub_order_nos for item in sublist]
        User.objects.filter(sub_order_no__in=sub_order_nos).delete()

        sub_order_no_list = [row.iloc[1].strip() for index, row in df.iterrows() if len(row.iloc[1].strip()) <= 20]
        User.objects.filter(sub_order_no__in=sub_order_no_list).delete()
        for index, row in df.iterrows():
            if len(row.iloc[1].strip()) > 20:
                sub_order_no_list = row.iloc[1].strip().split(";")
                for s in sub_order_no_list:
                    user = User(
                        sub_order_no=s,
                        product_quantity=1,
                        name=row.iloc[11],
                        order_total_amount=row.iloc[7],
                    )
                    user_list.append(user)
            else:
                user = User(
                    sub_order_no=row.iloc[1].strip(),
                    product_quantity=row.iloc[6],
                    name=row.iloc[11],
                    order_total_amount=row.iloc[7],
                )
                user_list.append(user)

        try:
            inserted_count = User.objects.bulk_create(user_list)
            return JsonResponse({'message': f'{len(inserted_count)} 条数据更新成功。'})
        except DatabaseError as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)


# 获取所有不带分页的汇总数据
class UserAll(ListAPIView):
    serializer_class = UserOrderSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        order_status = self.request.GET.get('order_status')
        search_date = self.request.GET.getlist("search_date[]")
        create_time = self.request.GET.get('create_time')
        season = self.request.GET.get('season')
        category = self.request.GET.get('category')
        day = self.request.GET.get('day')
        code = self.request.GET.get('code')
        if not search_date and order_status == "请选择订单状态":
            return User.objects.all()

        elif order_status == "千川订单":
            self.serializer_class = Search3Order
            queryset = search_3(order_status, search_date, code)
            queryset = [Search3Result(obj.id, obj.m, obj.sum_total_amount_3, obj.sum_product_quantity_3,
                                      obj.sum_total_amount_5, obj.sum_product_quantity_5,
                                      obj.pending_and_in_transit, obj.pending_and_in_transit_num,
                                      obj.returned, obj.returned_num, obj.inventory, obj.img) for obj in queryset]
        elif order_status == "客户信息排名":
            self.serializer_class = Search4Order
            queryset = search_4(order_status, search_date)
            queryset = [Search4Result(obj.id, obj.name, obj.first_day, obj.recently_day, obj.sum_orders,
                                      obj.success_money, obj.back_money, obj.wait_money, obj.transit_money,
                                      obj.back_rate, obj.success_num, obj.back_num, obj.wait_num, obj.transit_num,
                                      obj.success_rate, obj.real_rate, obj.not_day, obj.new_user, obj.sum_score
                                      ) for obj in queryset]
        elif order_status == "款号信息排名":
            self.serializer_class = Search5Order
            queryset = search_5(order_status, search_date, code)
            queryset = [Search5Result(obj.id, obj.name, obj.first_day, obj.recently_day, obj.sum_orders,
                                      obj.success_money, obj.back_money, obj.wait_money, obj.transit_money,
                                      obj.run_single, obj.category,
                                      obj.back_rate, obj.success_num, obj.back_num, obj.wait_num, obj.transit_num,
                                      obj.success_rate, obj.real_rate, obj.not_day, obj.inventory
                                      ) for obj in queryset]
        elif order_status == '老款大于5,30天没播':
            self.serializer_class = Search6Order
            queryset = search_6(create_time, season, category)
            queryset = [Search6Result(obj.id, obj.code, obj.category, obj.stock, obj.cost, obj.sales,
                                      obj.first_registration_time, obj.last_registration_time, obj.number,
                                      obj.create_time, obj.season
                                      ) for obj in queryset]
        elif order_status == '热销款':
            self.serializer_class = StockInSerializer
            queryset = search_7()
        elif order_status == '滞销款':
            self.serializer_class = StockInSerializer2
            queryset = search_8()
        elif order_status == '最近几天热卖':
            self.serializer_class = StockInSerializer3
            queryset = search_9(day)
        elif order_status == '库存1-5':
            self.serializer_class = Search10Order
            queryset = search_10(create_time, season, category)
            queryset = [Search10Result(obj.id, obj.merchant_code, obj.category, obj.date_time, obj.live_exposure_count,
                                       obj.one_live_deal_item_count, obj.quantity, obj.first_time,
                                       obj.last_time, obj.inventory, obj.live_deal_item_count, obj.create_time,
                                       obj.season
                                       ) for obj in queryset]
        elif order_status == '选款:30天全量表汇总':
            self.serializer_class = Search11Order
            queryset = search_11(code)
            queryset = [Search11Result(obj.id, obj.code, obj.category, obj.commodity_image, obj.inventory,
                                       obj.order_quantity, obj.price, obj.live_deal_item_count,
                                       obj.pre_shipment_refund_rate, obj.post_shipment_refund_rate,
                                       obj.order_submit_time,
                                       obj.one_live_exposure_count, obj.one_live_deal_item_count,
                                       obj.quantity, obj.first_registration_time, obj.last_registration_time
                                       ) for obj in queryset]
        elif order_status == '选款:爆款':
            self.serializer_class = StockInSerializer12
            queryset = search_12()
        return queryset


# 条件2


def search_3(order_status=None, search_date=None, code=None):
    start_date = '1999-05-07 00:00:00'
    end_date = '2100-05-08 00:00:00'

    if order_status == "千川订单" and search_date:
        start_date = search_date[0]
        end_date = search_date[1]
        start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
        end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d 23:59:59')
    if code is None or len(code) == 0:
        code = '%%'
    query = '''
        SELECT
        a.*,
        b.commodity_image
        FROM
        (
        SELECT
			a.*,
			b.inventory
			FROM
			(
        SELECT 
				NULL AS id, 
				m, 
				SUM(sum_total_amount_3) AS sum_total_amount_3, 
				SUM(sum_product_quantity_3) AS sum_product_quantity_3,
                SUM(sum_total_amount_5) AS sum_total_amount_5, 
				SUM(sum_product_quantity_5) AS sum_product_quantity_5,
				SUM(pending_and_in_transit) AS pending_and_in_transit,
				SUM(pending_and_in_transit_num) AS pending_and_in_transit_num,
				SUM(returned) AS returned,
				SUM(returned_num) AS returned_num
        FROM (
            SELECT 
            LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) AS m, 
            SUM(o.order_total_amount) AS sum_total_amount_3, 
            SUM(o.product_quantity) AS sum_product_quantity_3,
            0 AS sum_total_amount_5, 
            0 AS sum_product_quantity_5,
            0 AS pending_and_in_transit,
            0 AS pending_and_in_transit_num,
            0 AS returned,
            0 AS returned_num
            FROM taiwei_orders AS o
            WHERE o.order_status = '已关闭'
            AND o.after_sale_status LIKE '%%退款成功%%'
            AND (o.merchant_remark NOT LIKE '%%退货%%' AND o.merchant_remark NOT LIKE '%%拒收%%' AND o.merchant_remark NOT LIKE '%%退回%%')
            AND o.order_submit_time BETWEEN %s AND %s
            AND o.ad_channel = '直播'
            GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)

            UNION ALL

            SELECT 
            LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) AS m, 
            0 AS sum_total_amount_3, 
            0 AS sum_product_quantity_3,
            SUM(o.order_total_amount) AS sum_total_amount_5, 
            SUM(o.product_quantity) AS sum_product_quantity_5,
            0 AS pending_and_in_transit,
            0 AS pending_and_in_transit_num,
            0 AS returned,
            0 AS returned_num
            FROM taiwei_orders AS o
            WHERE o.order_status = '已完成'
            AND (o.after_sale_status LIKE '%%售后关闭%%' OR o.after_sale_status = '-')
            AND o.order_submit_time BETWEEN %s AND %s
            AND o.ad_channel = '直播'
            GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)
					 
					  UNION ALL
						
						SELECT 
						LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) AS m, 
						0 AS sum_total_amount_3, 
						0 AS sum_product_quantity_3,
            0 AS sum_total_amount_5, 
						0 AS sum_product_quantity_5,
						SUM(order_total_amount) as pending_and_in_transit,
						SUM(product_quantity) AS pending_and_in_transit_num,
						0 AS returned,
						0 AS returned_num
            FROM taiwei_orders AS o
						WHERE ((o.order_status = '已发货' AND (o.after_sale_status LIKE '%%售后关闭%%' OR o.after_sale_status = '-')) 
						OR (o.order_status = '待发货' AND o.after_sale_status = '-'))
            AND o.order_submit_time BETWEEN %s AND %s
            AND o.ad_channel = '直播'
            GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)
						
						
						UNION ALL
						
						SELECT 
						LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) AS m, 
						0 AS sum_total_amount_3, 
						0 AS sum_product_quantity_3,
            0 AS sum_total_amount_5, 
						0 AS sum_product_quantity_5,
						0 as pending_and_in_transit,
						0 AS pending_and_in_transit_num,
						SUM(order_total_amount) AS returned,
						SUM(product_quantity) AS returned_num
            FROM taiwei_orders AS o
						WHERE ((o.order_status = '已关闭' AND (o.after_sale_status LIKE '%%退款成功%%' AND 
						(o.merchant_remark LIKE '%%退货%%' OR o.merchant_remark LIKE '%%拒收%%' OR o.merchant_remark LIKE '%%退回%%'))) 
						OR (o.order_status = '已发货' AND 
						(o.after_sale_status LIKE '%%售后待处理%%' OR o.after_sale_status LIKE '%%待收退货%%' 
						OR o.after_sale_status LIKE '%%待退货%%' OR o.after_sale_status LIKE '%%退款成功%%' )) 
						OR (o.order_status='已完成' AND (o.after_sale_status LIKE '%%待收退货%%' OR o.after_sale_status LIKE '%%待退货%%' OR o.after_sale_status LIKE '%%退款成功%%')))
            AND o.order_submit_time BETWEEN %s AND %s
            AND o.ad_channel = '直播'
            GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)
										
        ) AS t
        GROUP BY m
        )as a
				LEFT JOIN
				(
					SELECT 
            code,
            SUM(inventory) AS inventory
        FROM taiwei_stock
        WHERE house = '泰维仓' OR house LIKE '意法%%'  OR house LIKE '茉雅%%'
        GROUP BY code
				)as b
				ON a.m=b.code
		) as a
		LEFT JOIN 
		(
		SELECT 
		LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) AS code, 
		MAX(c.commodity_image) as commodity_image
		FROM 
		taiwei_orders as o 
	    LEFT JOIN 
	    taiwei_commodity as c 
		on o.product_id=c.commodity_code 
		GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)
		)as b
		ON a.m = b.code
		WHERE m like %s
    '''

    queryset = Order.objects.raw(query, [start_date, end_date, start_date,
                                         end_date, start_date, end_date, start_date, end_date, code])

    return queryset


def search_4(order_status=None, search_date=None):
    start_date = '1999-05-07 00:00:00'
    if order_status == "客户信息排名" and search_date:
        start_date = search_date[0]
        start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')

    query = r'''
           SELECT 
           id, 
           name, 
           first_day, 
           recently_day, 
           sum_orders, 
           success_money, 
           back_money, 
           wait_money, 
           transit_money, 
           back_rate, 
           success_num, 
           back_num, 
           wait_num, 
           transit_num, 
           success_rate, 
           real_rate, 
           not_day, 
           new_user, 
           100 - ROUND(wait_rank / (MAX(wait_rank) OVER() / 100), 2)-0.5*COALESCE(back_num, 0)*back_rate AS sum_score				
            FROM(		
                    SELECT
            NULL as id,
            name,
            first_day,
            recently_day,
            sum_orders,
            success_money,
            back_money,
            wait_money,
            transit_money,
            back_rate,
            success_num,
            back_num,
            wait_num,
            transit_num,
            success_rate,
            real_rate,
            not_day,
            new_user,
            CASE
                 WHEN (success_rate IS NULL AND transit_money IS NULL) THEN NULL
                 ELSE DENSE_RANK() OVER (ORDER BY (COALESCE(real_rate, 0)+(0.35*COALESCE(transit_money, 0))) DESC) 
            END AS wait_rank
            FROM(
            SELECT 
            name,
            first_day,
            recently_day,
            sum_orders,
            success_money,
            back_money,
            wait_money,
            transit_money*(1-back_rate) as transit_money,
            back_rate,
            success_num,
            back_num,
            wait_num,
            transit_num,
            success_rate,
            real_rate,
            not_day,
            new_user
            FROM(
            SELECT
              name,
              DATE(MIN(first_day)) AS first_day,
              DATE(MAX(recently_day)) AS recently_day,
              MAX(sum_orders) AS sum_orders,
                MAX(success_money) AS success_money,
                MAX(back_money) AS back_money,
              MAX(wait_money) AS wait_money,
                MAX(transit_money) AS transit_money,
                CASE
                    WHEN (MAX(back_num) / (MAX(back_num) + MAX(success_num))) IS NULL THEN 0
                    ELSE MAX(back_num) / (MAX(back_num) + MAX(success_num)) 
                END AS back_rate,
                MAX(success_num) AS success_num,
                MAX(back_num) AS back_num,
              MAX(wait_num) AS wait_num,
              MAX(transit_num) AS transit_num,
              MAX(success_rate) AS success_rate,
                CASE
                WHEN (MAX(success_rate) IS NULL AND MAX(back_num)) IS NULL THEN NULL
                WHEN MAX(back_num) IS NULL THEN MAX(success_rate)
                WHEN (MAX(success_rate) IS NULL AND MAX(back_num) IS NOT NULL) THEN 0 - MAX(back_num) * 8.21
                ELSE MAX(success_rate) - MAX(back_num) * 8.21
              END AS real_rate,
							MAX(not_day) AS not_day,
                CASE
                WHEN DATEDIFF(CURDATE(), MIN(first_day)) < 7 THEN '7天新客'
                WHEN DATEDIFF(CURDATE(), MIN(first_day)) >= 7 AND DATEDIFF(CURDATE(),MIN(first_day)) <= 15 THEN '15天新客'
                ELSE NULL
                END as new_user
        FROM (
          -- 最早出现 和最近出现 和 未出现天数 和订单出现的天数
          SELECT
            u.name,
            MIN(o.order_submit_time) AS first_day,
            MAX(o.order_submit_time) AS recently_day,
            DATEDIFF(CURDATE(), MAX(o.order_submit_time)) AS not_day,
            COUNT(DISTINCT DATE(o.order_submit_time)) AS sum_orders,													
            NULL AS wait_money,
            NULL AS wait_num,
            NULL AS success_money,
            NULL AS success_num,
            NULL AS back_money,
            NULL AS back_num,
            NULL AS success_rate,
            NULL AS transit_money,
            NULL AS transit_num
          FROM
            `taiwei_user` AS u
            RIGHT JOIN taiwei_orders AS o ON u.sub_order_no = o.sub_order_no
          WHERE
            o.order_submit_time BETWEEN %s AND CURDATE()
          GROUP BY
            u.name

          UNION ALL

          -- 代发货金额和数量
          SELECT
            u.name,
            NULL AS first_day,
            NULL AS recently_day,
            NULL AS not_day,
            NULL AS sum_orders,
            SUM(o.order_total_amount) AS wait_money,
            SUM(o.product_quantity) AS wait_num,
            NULL AS success_money,
            NULL AS success_num,
            NULL AS back_money,
            NULL AS back_num,
            NULL AS success_rate,
            NULL AS transit_money,
            NULL AS transit_num
          FROM
            `taiwei_user` AS u
            RIGHT JOIN taiwei_orders AS o ON u.sub_order_no = o.sub_order_no
          WHERE
            o.order_status = '待发货'
            AND o.after_sale_status = '-'
            AND o.order_submit_time BETWEEN %s AND CURDATE()
          GROUP BY
            u.`name`

          UNION ALL

          -- 成功金额 和数量
          SELECT
            u.name,
            NULL AS first_day,
            NULL AS recently_day,
            NULL AS not_day,
            NULL AS sum_orders,
            NULL AS wait_money,
            NULL AS wait_num,
            SUM(o.order_total_amount) AS success_money,
            SUM(o.product_quantity) AS success_num,
            NULL AS back_money,
            NULL AS back_num,
            NULL AS success_rate,
            NULL AS transit_money,
            NULL AS transit_num
          FROM
            `taiwei_user` AS u
            RIGHT JOIN taiwei_orders AS o ON u.sub_order_no = o.sub_order_no
          WHERE
            (o.order_status = '已完成' AND (o.after_sale_status LIKE '%%售后关闭%%' OR o.after_sale_status = '-'))
            AND o.order_submit_time BETWEEN %s AND CURDATE()
          GROUP BY
            u.`name`

          UNION ALL

          -- 退回金额和退回数量
          SELECT
            u.name, 
            NULL AS first_day,
            NULL AS recently_day,
            NULL AS not_day,
            NULL AS sum_orders,
            NULL AS wait_money,
            NULL AS wait_num,
            NULL AS success_money,
            NULL AS success_num,
            SUM(o.order_total_amount) AS back_money,
            SUM(o.product_quantity) AS back_num,
            NULL AS success_rate,
            NULL AS transit_money,
            NULL AS transit_num
          FROM
            `taiwei_user` AS u
            RIGHT JOIN taiwei_orders AS o ON u.sub_order_no = o.sub_order_no
          WHERE
            (
              (o.order_status = '已关闭' AND (o.after_sale_status LIKE '%%退款成功%%' AND (o.merchant_remark LIKE '%%退货%%' OR o.merchant_remark LIKE '%%拒收%%' OR o.merchant_remark LIKE '%%退回%%')))
              OR (o.order_status = '已发货' AND (o.after_sale_status LIKE '%%售后待处理%%' OR o.after_sale_status LIKE '%%待收退货%%' OR o.after_sale_status LIKE '%%待退货%%' OR o.after_sale_status LIKE '%%退款成功%%'))
              OR (o.order_status = '已完成' AND (o.after_sale_status LIKE '%%待收退货%%' OR o.after_sale_status LIKE '%%待退货%%' OR o.after_sale_status LIKE '%%退款成功%%'))
            )
            AND o.order_submit_time BETWEEN %s AND CURDATE()
          GROUP BY
            u.`name`

          UNION ALL

          -- 成功利润 和利润排名 和利润得分
          SELECT
             name,
           NULL AS first_day,
           NULL AS recently_day,
           NULL AS not_day,
           NULL AS sum_orders,
           NULL AS wait_money,
           NULL AS wait_num,
           NULL AS success_money,
           NULL AS success_num,
           NULL AS back_money,
           NULL AS back_num,
           success_rate,
           NULL AS transit_money,
           NULL AS transit_num

        FROM (
        SELECT
            name,
            success_rate
          FROM (
            SELECT
              u.name,
              SUM(
                o.order_total_amount - ROUND(
                  CASE
                    WHEN COALESCE(g.price, 0) = 0 OR g.price IS NULL THEN o.product_amount/2
                    ELSE COALESCE(g.price, 0)
                  END,
                  2
                ) * u.product_quantity
              ) AS success_rate
            FROM
              taiwei_user AS u
              RIGHT JOIN taiwei_orders AS o ON u.sub_order_no = o.sub_order_no
              LEFT JOIN taiwei_goods AS g ON LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) = g.merchant_code
            WHERE
              (o.order_status = '已完成' AND (o.after_sale_status LIKE '%%售后关闭%%' OR o.after_sale_status = '-'))
              AND o.order_submit_time BETWEEN %s AND CURDATE()
            GROUP BY
              u.name
          ) AS subquery1
        ) AS subquery2


          UNION ALL

          -- 在途金额和数量和在途排名和在途得分
          SELECT 
            name,
            NULL AS first_day,
            NULL AS recently_day,
            NULL AS not_day,
            NULL AS sum_orders,
            NULL AS wait_money,
            NULL AS wait_num,
            NULL AS success_money,
            NULL AS success_num,
            NULL AS back_money,
            NULL AS back_num,
            NULL AS success_rate,
            transit_money,
            transit_num
          FROM(
            SELECT 
                name,
                transit_money,
                transit_num
            FROM(
              SELECT
                u.name,
                SUM(o.order_total_amount) AS transit_money,
                SUM(o.product_quantity) AS transit_num
              FROM
                `taiwei_user` AS u
                RIGHT JOIN taiwei_orders AS o ON u.sub_order_no = o.sub_order_no
              WHERE
                  (o.order_status = '已发货' AND (o.after_sale_status = '-' OR o.after_sale_status LIKE '%%售后关闭'))
                  AND o.order_submit_time BETWEEN %s AND CURDATE()
              GROUP BY
              u.name
            ) AS subquery1
           ) AS subquery2
        ) AS merged_data
        GROUP BY name
        ) AS　merged_data
        ) AS　merged_data2
				) AS　merged_data3
        ORDER BY success_money DESC
    '''

    queryset = Order.objects.raw(query, [start_date, start_date, start_date, start_date, start_date, start_date])

    return queryset


def search_5(order_status=None, search_date=None, code=None):
    start_date = '1999-05-07 00:00:00'
    if order_status == "款号信息排名" and search_date:
        start_date = search_date[0]
        start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d 00:00:00')
    if code is None or len(code) == 0:
        code = '%%'
    query = '''
        SELECT
        a.*,
        b.inventory
        FROM(
        SELECT
          NULL AS id,
          name,
          DATE(MIN(first_day)) AS first_day,
          DATE(MAX(recently_day)) AS recently_day,
          MAX(sum_orders) AS sum_orders,
            MAX(success_money) AS success_money,
            MAX(back_money) AS back_money,
          MAX(wait_money) AS wait_money,
            MAX(transit_money) AS transit_money,
            MAX(run_single)  AS run_single,
            MAX(category) as category,
            MAX(back_num) / (MAX(back_num) + MAX(success_num)) AS back_rate,
            MAX(success_num) AS success_num,
            MAX(back_num) AS back_num,
          MAX(wait_num) AS wait_num,
          MAX(transit_num) AS transit_num,
          MAX(success_rate) AS success_rate,
            CASE
            WHEN (MAX(success_rate) IS NULL AND MAX(back_num)) IS NULL THEN NULL
            WHEN MAX(back_num) IS NULL THEN MAX(success_rate)
            WHEN (MAX(success_rate) IS NULL AND MAX(back_num) IS NOT NULL) THEN 0 - MAX(back_num) * 8.21
            ELSE MAX(success_rate) - MAX(back_num) * 8.21
          END AS real_rate,
            MAX(not_day) AS not_day
            
          
        
        FROM (
          -- 最早出现 和最近出现 和 未出现天数 和订单出现的天数
          SELECT
            LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) as name,
            MIN(o.order_submit_time) AS first_day,
            MAX(o.order_submit_time) AS recently_day,
            DATEDIFF(CURDATE(), MAX(o.order_submit_time)) AS not_day,
            COUNT(DISTINCT DATE(o.order_submit_time)) AS sum_orders,													
            NULL AS wait_money,
            NULL AS wait_num,
            NULL AS success_money,
            NULL AS success_num,
            NULL AS back_money,
            NULL AS back_num,
            NULL AS success_rate,
            NULL AS transit_money,
            NULL AS transit_num,	
            NULL AS run_single,
            REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(o.product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
          FROM
            `taiwei_user` AS u
            RIGHT JOIN taiwei_orders AS o ON u.sub_order_no = o.sub_order_no
          WHERE
            o.order_submit_time BETWEEN %s AND CURDATE()
          GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)
        
          UNION ALL
        
          -- 代发货金额和数量
          SELECT
            LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) as name,
            NULL AS first_day,
            NULL AS recently_day,
            NULL AS not_day,
            NULL AS sum_orders,
            SUM(o.product_amount) AS wait_money,
            SUM(o.product_quantity) AS wait_num,
            NULL AS success_money,
            NULL AS success_num,
            NULL AS back_money,
            NULL AS back_num,
            NULL AS success_rate,
            NULL AS transit_money,
            NULL AS transit_num,	
            NULL AS run_single,
            REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(o.product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
          FROM
            `taiwei_user` AS u
            RIGHT JOIN taiwei_orders AS o ON u.sub_order_no = o.sub_order_no
          WHERE
            o.order_status = '待发货'
            AND o.after_sale_status = '-'
            AND o.order_submit_time BETWEEN %s AND CURDATE()
          GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)
        
          UNION ALL
        
          -- 成功金额 和数量
          SELECT
            LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) as name,
            NULL AS first_day,
            NULL AS recently_day,
            NULL AS not_day,
            NULL AS sum_orders,
            NULL AS wait_money,
            NULL AS wait_num,
            SUM(o.order_total_amount) AS success_money,
            SUM(o.product_quantity) AS success_num,
            NULL AS back_money,
            NULL AS back_num,
            NULL AS success_rate,
            NULL AS transit_money,
            NULL AS transit_num,	
            NULL AS run_single,
            REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(o.product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
          FROM
            `taiwei_user` AS u
            RIGHT JOIN taiwei_orders AS o ON u.sub_order_no = o.sub_order_no
          WHERE
            (o.order_status = '已完成' AND (o.after_sale_status LIKE '%%售后关闭%%' OR o.after_sale_status = '-'))
            AND o.order_submit_time BETWEEN %s AND CURDATE()
          GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)
        
          UNION ALL
        
          -- 退回金额和退回数量
          SELECT
            LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) as name,
            NULL AS first_day,
            NULL AS recently_day,
            NULL AS not_day,
            NULL AS sum_orders,
            NULL AS wait_money,
            NULL AS wait_num,
            NULL AS success_money,
            NULL AS success_num,
            SUM(o.order_total_amount) AS back_money,
            SUM(o.product_quantity) AS back_num,
            NULL AS success_rate,
            NULL AS transit_money,
            NULL AS transit_num,
            NULL AS run_single,
            REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(o.product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category	
          FROM
            `taiwei_user` AS u
            RIGHT JOIN taiwei_orders AS o ON u.sub_order_no = o.sub_order_no
          WHERE
            (
              (o.order_status = '已关闭' AND (o.after_sale_status LIKE '%%退款成功%%' AND (o.merchant_remark LIKE '%%退货%%' OR o.merchant_remark LIKE '%%拒收%%' OR o.merchant_remark LIKE '%%退回%%')))
              OR (o.order_status = '已发货' AND (o.after_sale_status LIKE '%%售后待处理%%' OR o.after_sale_status LIKE '%%待收退货%%' OR o.after_sale_status LIKE '%%待退货%%' OR o.after_sale_status LIKE '%%退款成功%%'))
              OR (o.order_status = '已完成' AND (o.after_sale_status LIKE '%%待收退货%%' OR o.after_sale_status LIKE '%%待退货%%' OR o.after_sale_status LIKE '%%退款成功%%'))
            )
            AND o.order_submit_time BETWEEN %s AND CURDATE()
          GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)
        
         UNION ALL
         
        SELECT 
        LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) as name,
        NULL AS first_day,
        NULL AS recently_day,
        NULL AS not_day,
        NULL AS sum_orders,
        NULL AS wait_money,
        NULL AS wait_num,
        NULL AS success_money,
        NULL AS success_num,
        NULL AS back_money,
        NULL AS back_num, 
        NULL AS success_rate,
        NULL AS transit_money,
        NULL AS transit_num,
        SUM(o.product_quantity) AS run_single,
        REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(o.product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
        FROM taiwei_orders AS o
        WHERE o.order_status = '已关闭'
        AND o.after_sale_status LIKE '%%退款成功%%'
        AND (o.merchant_remark NOT LIKE '%%退货%%' AND o.merchant_remark NOT LIKE '%%拒收%%' AND o.merchant_remark NOT LIKE '%%退回%%')
        AND o.order_submit_time BETWEEN %s AND CURDATE()
        GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)
  
          UNION ALL
        
          -- 成功利润 和利润排名 和利润得分
          SELECT
             name,
           NULL AS first_day,
           NULL AS recently_day,
           NULL AS not_day,
           NULL AS sum_orders,
           NULL AS wait_money,
           NULL AS wait_num,
           NULL AS success_money,
           NULL AS success_num,
           NULL AS back_money,
           NULL AS back_num,
           success_rate,
           NULL AS transit_money,
           NULL AS transit_num,
           NULL AS run_single,
           category
        FROM (     
            SELECT
              LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) as name,
              REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(o.product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category,	
              SUM(
                o.order_total_amount - ROUND(
                  CASE
                    WHEN COALESCE(g.price, 0) = 0 OR g.price IS NULL THEN o.product_amount/2
                    ELSE COALESCE(g.price, 0)
                  END,
                  2
                ) * u.product_quantity
              ) AS success_rate
            FROM
              taiwei_user AS u
              RIGHT JOIN taiwei_orders AS o ON u.sub_order_no = o.sub_order_no
              LEFT JOIN taiwei_goods AS g ON LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) = g.merchant_code
            WHERE
              (o.order_status = '已完成' AND (o.after_sale_status LIKE '%%售后关闭%%' OR o.after_sale_status = '-'))
              AND o.order_submit_time BETWEEN %s AND CURDATE()
            GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)
          ) AS subquery1
        
         
        
          UNION ALL
        
          -- 在途金额和数量和在途排名和在途得分
          SELECT 
            name,
            NULL AS first_day,
            NULL AS recently_day,
            NULL AS not_day,
            NULL AS sum_orders,
            NULL AS wait_money,
            NULL AS wait_num,
            NULL AS success_money,
            NULL AS success_num,
            NULL AS back_money,
            NULL AS back_num,
            NULL AS success_rate,
            transit_money,
            transit_num,
            NULL AS run_single,
            category
            FROM(
              SELECT
                LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) as name,
                SUM(u.order_total_amount) AS transit_money,
                SUM(u.product_quantity) AS transit_num,
                REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(o.product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category         
              FROM
                `taiwei_user` AS u
                RIGHT JOIN taiwei_orders AS o ON u.sub_order_no = o.sub_order_no
              WHERE
                  (o.order_status = '已发货' AND (o.after_sale_status = '-' OR o.after_sale_status LIKE '%%售后关闭'))
                  AND o.order_submit_time BETWEEN %s AND CURDATE()
              GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)
            ) AS subquery1
        ) AS merged_data
        WHERE name LIKE %s
        GROUP BY name
        ORDER BY success_money DESC
        )as a
        LEFT JOIN
        (
            SELECT
            MAX(cls) as cls,
            code,
            (SUM(CASE WHEN house IN ('泰维仓', '茉雅丰岭仓', '意法仓') THEN inventory ELSE 0 END) - SUM(order_quantity)) as inventory
            FROM 
            taiwei_newstock
            GROUP BY code
        )as b
        ON a.name = b.code
    '''
    queryset = Order.objects.raw(query,
                                 [start_date, start_date, start_date, start_date, start_date, start_date, start_date,
                                  code])

    return queryset


def search_6(create_time=None, season=None, category=None):
    if category is None:
        category = "%"
    else:
        category = '%' + category + '%'
    create_time1 = '2010'
    create_time2 = '2030'
    if create_time:
        create_time1 = create_time.split('-')[0]
        create_time2 = create_time.split('-')[1]
    new_season = '%%'
    if season:
        new_season = season
    query = '''
    SELECT
		NULL as id,
		a.code,
		a.category,
		a.stock,
		a.cost,
		a.sales,
		b.first_registration_time,
		b.last_registration_time,
		a.number,
		a.create_time,
		a.season
		FROM
		(
        SELECT 
        NUll as id,
        g.merchant_code as code,
        g.category,
        s.inventory as stock,
        g.price as cost,
        p.quantity as sales,
        s.number as number,
        DATE(g.create_time) as create_time,
        g.season as season
		FROM taiwei_goods as g
		RIGHT JOIN 
		(SELECT code,sum(inventory) as inventory,
		SUM(order_quantity) as order_quantity,
		SUM(waiting_quantity) as waiting_quantity,
		SUM(orderable) as orderable,
		SUM(shippable) as shippable,
		SUM(number) as number
		 FROM 
		 taiwei_stock WHERE house='泰维仓' or house='茉雅丰岭仓' or house='意法仓' GROUP BY code
		 HAVING inventory > 5)
		 as s on g.merchant_code = s.code
		LEFT JOIN
		(SELECT DISTINCT  LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) as code,
		 SUM(live_deal_item_count) as live_deal_item_count
		FROM taiwei_commodity as c
		LEFT JOIN taiwei_orders as o
		ON c.commodity_code = o.product_id
		GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) )
		as o on o.code = g.merchant_code
		LEFT JOIN 
		(SELECT product_code,sum(quantity) as quantity
		FROM taiwei_salesrecord
		WHERE transaction_time >= CURDATE() - INTERVAL 15 DAY
		GROUP BY product_code) as p
		ON p.product_code = g.merchant_code
		WHERE g.season LIKE %s
		AND YEAR(create_time) BETWEEN %s AND %s
		AND (o.code IS NULL OR o.live_deal_item_count<=2)
		AND g.category LIKE %s	
	)as a
	LEFT JOIN
		(SELECT
		product_code,
		DATE(MIN(registration_time)) as first_registration_time,
        DATE(MAX(registration_time)) as last_registration_time 
		FROM 
		taiwei_stock_in
		GROUP BY product_code
		) as b 
		ON a.code = b.product_code
    '''
    queryset = Goods.objects.raw(query, [new_season, create_time1, create_time2, category])
    return queryset


def search_7():
    query = '''
    SELECT 
        NULL as id,
        s.code as product_code,
        t.count_quantity,
        t.quantity,
        t.product_name as product_name,
        s.inventory as inventory,
        t.first_registration_time,
        t.last_registration_time
    FROM(
        SELECT 
            code,
            SUM(inventory) AS inventory
        FROM taiwei_stock
        WHERE house = '泰维仓' OR house LIKE '意法%%'  OR house LIKE '茉雅%%'
        GROUP BY code
    ) AS s
    RIGHT JOIN(
        SELECT 
        t.product_code as product_code,
        MAX(t.product_name) as product_name,
        MAX(t.specification) as specification,
        COUNT(t.registration_time) as count_quantity,
        SUM(t.quantity) as quantity,
        MAX(t.reason) as reason,
        MAX(t.handler) as handler,
        DATE(MIN(t.registration_time)) as first_registration_time,
        DATE(MAX(t.registration_time)) as last_registration_time
        FROM taiwei_stock_in AS t
        JOIN (
            SELECT product_code, COUNT(DISTINCT DATE(registration_time)) AS registration_time
            FROM taiwei_stock_in
            GROUP BY product_code
            HAVING registration_time >= 3
        ) AS subquery
        ON t.product_code = subquery.product_code
        GROUP BY t.product_code
        ORDER BY last_registration_time DESC
    ) AS t ON s.code = t.product_code
    '''
    queryset = StockIn.objects.raw(query)
    return queryset


def search_8():
    query = '''
        SELECT
				NULL as id,
				a.product_code,
				a.count_quantity,
				a.quantity,
				d.category as product_name,
				c.inventory,
				a.first_registration_time,
				a.last_registration_time
				FROM
				(
				SELECT
				product_code,
				COUNT(DISTINCT(DATE(registration_time))) as count_quantity,
				SUM(quantity) as quantity,
				DATE(MIN(registration_time)) as first_registration_time,
                DATE(MAX(registration_time)) as last_registration_time
				FROM taiwei_stock_in
				WHERE registration_time <= CURDATE() - INTERVAL 6 DAY
				GROUP BY product_code
				) as a
				
				LEFT JOIN
				(
				SELECT
				MAX(product_name) as product_name,
				MAX(product_code) as product_code,
				COUNT(DISTINCT(CASE WHEN transaction_time>= CURDATE() - INTERVAL 15 DAY THEN recipient ELSE NULL END)) as recipient,
				SUM(CASE WHEN transaction_time>= CURDATE() - INTERVAL 15 DAY THEN quantity ELSE 0 END) as quantity
				FROM 
				taiwei_salesrecord 
				GROUP BY product_code
				HAVING
				recipient <= 2 AND quantity < 10
				)as b
				ON a.product_code = b.product_code
				LEFT JOIN
				(
				SELECT 
        code,
        SUM(inventory) AS inventory
        FROM taiwei_stock
        WHERE house = '泰维仓' OR house LIKE '意法%%'  OR house LIKE '茉雅%%'
        GROUP BY code
				)as c
				ON a.product_code = c.code
				
				LEFT JOIN
				(
					SELECT 
                   merchant_code,
                   category
                   FROM 
                   taiwei_goods
				)as d
				ON a.product_code = d.merchant_code
		
				WHERE
				b.recipient IS NOT NULL
    '''
    queryset = StockIn.objects.raw(query)
    return queryset


def search_9(day=None):
    if day is None:
        day = 3
    query = '''
        SELECT
            NULL as id,
            a.code,
            a.category,
            a.product_amount as price,
            a.commodity_image,
            c.inventory,
            c.order_quantity,
            d.live_deal_item_count,
            d.live_deal_conversion_rate
            FROM
            (     
            SELECT
			MAX(a.commodity_image) as commodity_image,
			MAX(a.commodity_code) as commodity_code,
			MAX(a.live_deal_amount) as live_deal_amount,
			b.code as code,
			MIN(b.product_amount) as product_amount,
			MAX(b.category) as category
			FROM
		
			(
			SELECT 
            commodity_code,
            MAX(commodity_image) as commodity_image,
            MAX(live_deal_amount) as live_deal_amount 
            FROM 
                    (
                    SELECT 
                            commodity_code,
                            commodity_image,
                            live_deal_amount
                    FROM 
                            taiwei_onecommodity
                    WHERE date_time >= CURDATE() - INTERVAL %s DAY
                    ORDER BY live_deal_amount DESC
                    LIMIT %s
                    ) AS subquery
            GROUP BY commodity_code
						) as a
            
            LEFT JOIN
            
            (SELECT 
                LEFT(merchant_code, LENGTH(merchant_code) - 1) AS code, 
                product_amount,
                product_id,
                REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(product_name, '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
            FROM 
            taiwei_orders
            ) as b
            on a.commodity_code = b.product_id
		    GROUP BY b.code
            
            )   as a    
            LEFT JOIN
            (
            SELECT 
                code,
                SUM(order_quantity) AS order_quantity,
                SUM(CASE WHEN house LIKE '%%泰维仓%%' OR house LIKE '%%意法%%' OR house LIKE '%%茉雅%%' THEN inventory ELSE 0 END) AS inventory
            FROM taiwei_stock
            GROUP BY code
            )as c
            ON a.code = c.code
            
            LEFT JOIN
            (
            SELECT
                live_deal_item_count,
                live_deal_conversion_rate,
                commodity_code
            FROM
            taiwei_commodity
             )as d   
             ON d.commodity_code = a.commodity_code
            
    '''
    queryset = Stock.objects.raw(query, [day, int(day) * 5])
    return queryset


def search_10(create_time=None, season=None, category=None):
    if category is None:
        category = "%"
    else:
        category = '%' + category + '%'
    create_time1 = '2010'
    create_time2 = '2030'
    if create_time:
        create_time1 = create_time.split('-')[0]
        create_time2 = create_time.split('-')[1]
    new_season = '%%'
    if season:
        new_season = season
    query = '''
        SELECT
    NULL as id,
		a.merchant_code,
		a.category,
		DATE(e.date_time) as date_time,
		e.live_exposure_count,
		e.one_live_deal_item_count,
		c.quantity,
		DATE(d.first_time) as first_time,
		DATE(d.last_time) as last_time,
		b.inventory,
		e.live_deal_item_count,
		a.create_time,
		a.season
		FROM
		(
		SELECT 
		merchant_code,
		category,
		DATE(create_time) as create_time,
		season
		FROM 
		taiwei_goods
		WHERE season LIKE %s
		AND YEAR(create_time) BETWEEN %s AND %s
		AND category LIKE %s
		) as a

		LEFT JOIN
		(
		SELECT 
		code,
		SUM(inventory) as inventory
		FROM 
		taiwei_stock
		WHERE house IN ('泰维仓', '茉雅丰岭仓', '意法仓') 
		GROUP BY code 
		) as b
		ON a.merchant_code = b.code
	
		LEFT JOIN
		(	
		SELECT 
		product_code,
		SUM(quantity) as quantity
		FROM 
		taiwei_salesrecord 
		WHERE DATE(transaction_time)>= CURDATE() - INTERVAL 15 DAY
		GROUP BY product_code
		) as c
		ON b.code = c.product_code
		LEFT JOIN
		(
		SELECT 
		product_code,
		MIN(registration_time) first_time,
		MAX(registration_time) last_time
		FROM taiwei_stock_in
		GROUP BY product_code
		) as d
		ON c.product_code = d.product_code
			
		LEFT JOIN
		(	 
		SELECT   
		c.*,
		LEFT(o.merchant_code, LENGTH(merchant_code) - 1) as merchant_code
		FROM
		(	 
			SELECT
				oc.code,
				oc.date_time,
				oc.live_exposure_count,
				oc.live_deal_item_count as one_live_deal_item_count,
				c.live_deal_item_count as live_deal_item_count
				FROM(
				SELECT
				MAX(date_time) as date_time,
				commodity_code as code,
				AVG(CASE WHEN live_exposure_count>200 THEN live_exposure_count ELSE NULL END) as live_exposure_count,
				AVG(live_deal_item_count)as live_deal_item_count
				FROM
				taiwei_onecommodity
				WHERE 
				date_time >=  CURDATE() - INTERVAL 5 DAY
				GROUP BY commodity_code
			) as oc
			LEFT JOIN
			(
				SELECT 
					commodity_code,
					live_deal_item_count 
					FROM taiwei_commodity
			) as c
			ON oc.code = c.commodity_code
		)as c	 
		 
		 LEFT JOIN
			(
				SELECT
				product_id,
				MAX(merchant_code) as merchant_code
				FROM 
				taiwei_orders
				GROUP BY product_id
			)as o
			ON c.code = o.product_id
			) as e
			ON d.product_code = e.merchant_code
		 WHERE b.inventory BETWEEN 1 AND 5
    '''
    queryset = Goods.objects.raw(query, [new_season, create_time1, create_time2, category])
    return queryset


def search_11(code=None):
    if code is None or len(code) == 0:
        code = '%%'
    query = """
        SELECT
        NULL as id,
		a.code,
		a.category,
		a.commodity_image,
		c.inventory,
		c.order_quantity,
		a.price,
		a.live_deal_item_count,
		a.pre_shipment_refund_rate,
		a.post_shipment_refund_rate,
		a.order_submit_time,
		d.live_exposure_count as one_live_exposure_count,
		d.live_deal_item_count as one_live_deal_item_count,
		f.quantity,
		DATE(e.first_registration_time) as first_registration_time,
		DATE(e.last_registration_time) as last_registration_time
		FROM
		(
		SELECT
		MAX(a.commodity_image) as commodity_image,
		MAX(a.live_deal_item_count)as live_deal_item_count,
		MAX(a.pre_shipment_refund_rate) as pre_shipment_refund_rate,
		MAX(a.post_shipment_refund_rate) as post_shipment_refund_rate,
		MAX(b.code) as code,
		AVG(b.price)as price,
		b.product_id as product_id,
		MIN(b.order_submit_time) as order_submit_time,
		MAX(b.category) as category
		FROM
		(
		SELECT 
		commodity_code,
		commodity_image,
		live_deal_item_count,
		pre_shipment_refund_rate,
		post_shipment_refund_rate
		FROM taiwei_commodity
		)as a
		LEFT JOIN
		(
		SELECT 
		LEFT(merchant_code, LENGTH(merchant_code) - 1) AS code,
		order_total_amount as price,
		product_id,
		order_submit_time,
		REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(product_name, '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
		FROM
		taiwei_orders
		)as b
		ON a.commodity_code = b.product_id
		GROUP BY b.product_id
		)as a
		
		LEFT JOIN
		(
		SELECT 
		code,
		SUM(CASE WHEN house IN ('泰维仓', '茉雅丰岭仓', '意法仓') THEN inventory ELSE 0 END) AS inventory,
		SUM(order_quantity) as order_quantity
		FROM taiwei_stock
		GROUP BY code
		)as c
		ON c.code = a.code
		
		LEFT JOIN
		(
			SELECT
            commodity_code,
            AVG(CASE WHEN live_exposure_count>200 THEN live_exposure_count ELSE NULL END) as live_exposure_count,
            AVG(live_deal_item_count)as live_deal_item_count
            FROM
            taiwei_onecommodity
            WHERE 
            date_time >=  CURDATE() - INTERVAL 5 DAY
            GROUP BY commodity_code
            HAVING live_deal_item_count>0
		)as d
		ON a.product_id = d.commodity_code
		LEFT JOIN
		(
			SELECT
			product_code,
			MIN(registration_time) as first_registration_time,
			MAX(registration_time) as last_registration_time
			FROM 
			taiwei_stock_in
			GROUP BY product_code
		)as e
		ON a.code = e.product_code
		LEFT JOIN
		(
			SELECT
			product_code,
			SUM(quantity) as quantity
			FROM
			taiwei_salesrecord
			WHERE transaction_time >=  CURDATE() - INTERVAL 15 DAY
			GROUP BY product_code	
		)as f
		ON a.code = f.product_code
		WHERE a.code LIKE %s
		ORDER BY live_deal_item_count desc
    """
    queryset = Order.objects.raw(query, [code])
    return queryset


def search_12():
    query = '''
        SELECT
            NULL as id,
            b.code,
            b.category,
            b.product_amount as price,
            a.commodity_image,
            c.inventory,
            c.order_quantity,
            a.live_deal_item_count,
            a.live_deal_conversion_rate,
            a.date_time
            FROM
            (
            SELECT 
                    *
            FROM (
                    SELECT 
                            *,
                            RANK() OVER(PARTITION BY DATE(date_time) ORDER BY deal_amount DESC) AS daily_rank
                    FROM 
                            taiwei_onecommodity
                            
            ) AS subquery
            WHERE 
                    daily_rank <= 10
                    AND (live_click_count/live_exposure_count) >0.24
                    AND (live_deal_user_count / live_click_count) > 0.04
                    AND date_time >= CURDATE() - INTERVAL 15 DAY
            ) as a
            LEFT JOIN
            (
                SELECT 
                        LEFT(MAX(merchant_code), LENGTH(MAX(merchant_code)) - 1) AS code, 
                        MAX(product_amount) as product_amount,
                        product_id,
                        REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
                FROM 
                taiwei_orders
                GROUP BY product_id
                ) as b
                on a.commodity_code = b.product_id
                LEFT JOIN
                (
                SELECT 
                        code,
                        SUM(order_quantity) AS order_quantity,
                        SUM(CASE WHEN house LIKE '%%泰维仓%%' OR house LIKE '%%意法%%' OR house LIKE '%%茉雅%%' THEN inventory ELSE 0 END) AS inventory
                FROM taiwei_stock
                GROUP BY code
                )as c
                ON b.code = c.code
    '''
    queryset = Stock.objects.raw(query)
    return queryset


# 获取汇总数据
class SummaryView(ListAPIView):
    # 获取带有分页的数据
    serializer_class = UserOrderSerializer
    pagination_class = OrderPagination

    def get_queryset(self):
        queryset = User.objects.all()
        order_status = self.request.GET.get('order_status')
        search_date = self.request.GET.getlist("search_date[]")
        create_time = self.request.GET.get('create_time')
        season = self.request.GET.get('season')
        category = self.request.GET.get('category')
        day = self.request.GET.get('day')
        code = self.request.GET.get('code')
        if not search_date and order_status == "请选择订单状态":
            return User.objects.all()

        elif order_status == "千川订单":
            self.serializer_class = Search3Order
            queryset = search_3(order_status, search_date, code)
            queryset = [Search3Result(obj.id, obj.m, obj.sum_total_amount_3, obj.sum_product_quantity_3,
                                      obj.sum_total_amount_5, obj.sum_product_quantity_5,
                                      obj.pending_and_in_transit, obj.pending_and_in_transit_num,
                                      obj.returned, obj.returned_num, obj.inventory, obj.commodity_image) for obj in
                        queryset]
        elif order_status == "客户信息排名":
            self.serializer_class = Search4Order
            queryset = search_4(order_status, search_date)
            queryset = [Search4Result(obj.id, obj.name, obj.first_day, obj.recently_day, obj.sum_orders,
                                      obj.success_money, obj.back_money, obj.wait_money, obj.transit_money,
                                      obj.back_rate, obj.success_num, obj.back_num, obj.wait_num, obj.transit_num,
                                      obj.success_rate, obj.real_rate, obj.not_day, obj.new_user, obj.sum_score
                                      ) for obj in queryset]
        elif order_status == "款号信息排名":
            self.serializer_class = Search5Order
            queryset = search_5(order_status, search_date, code)
            queryset = [Search5Result(obj.id, obj.name, obj.first_day, obj.recently_day, obj.sum_orders,
                                      obj.success_money, obj.back_money, obj.wait_money, obj.transit_money,
                                      obj.run_single, obj.category,
                                      obj.back_rate, obj.success_num, obj.back_num, obj.wait_num, obj.transit_num,
                                      obj.success_rate, obj.real_rate, obj.not_day, obj.inventory
                                      ) for obj in queryset]
        elif order_status == '老款大于5,30天没播':
            self.serializer_class = Search6Order
            queryset = search_6(create_time, season, category)
            queryset = [Search6Result(obj.id, obj.code, obj.category, obj.stock, obj.cost, obj.sales,
                                      obj.first_registration_time, obj.last_registration_time, obj.number,
                                      obj.create_time, obj.season
                                      ) for obj in queryset]
        elif order_status == '热销款':
            self.serializer_class = StockInSerializer
            queryset = search_7()
        elif order_status == '滞销款':
            self.serializer_class = StockInSerializer2
            queryset = search_8()
        elif order_status == '最近几天热卖':
            self.serializer_class = StockInSerializer3
            queryset = search_9(day)
        elif order_status == '库存1-5':
            self.serializer_class = Search10Order
            queryset = search_10(create_time, season, category)
            queryset = [Search10Result(obj.id, obj.merchant_code, obj.category, obj.date_time, obj.live_exposure_count,
                                       obj.one_live_deal_item_count, obj.quantity, obj.first_time,
                                       obj.last_time, obj.inventory, obj.live_deal_item_count, obj.create_time,
                                       obj.season
                                       ) for obj in queryset]
        elif order_status == '选款:30天全量表汇总':
            self.serializer_class = Search11Order
            queryset = search_11(code)
            queryset = [Search11Result(obj.id, obj.code, obj.category, obj.commodity_image, obj.inventory,
                                       obj.order_quantity, obj.price, obj.live_deal_item_count,
                                       obj.pre_shipment_refund_rate, obj.post_shipment_refund_rate,
                                       obj.order_submit_time,
                                       obj.one_live_exposure_count, obj.one_live_deal_item_count,
                                       obj.quantity, obj.first_registration_time, obj.last_registration_time
                                       ) for obj in queryset]
        elif order_status == '选款:爆款':
            self.serializer_class = StockInSerializer12
            queryset = search_12()
        return queryset


class UpdateGoods(APIView):
    # 上传货品档案
    def post(self, request):
        excel_file = request.data.get('excel-file')
        if not excel_file:
            return Response({'error': '文件未上传'}, status=400)

            # 处理Excel文件，提取数据或存储到数据库
        df = pd.read_excel(excel_file, header=0)
        goods_list = []

        for index, row in df.iterrows():

            if row["固定成本价"] == '-':
                row["固定成本价"] = 0

            goods = Goods(
                merchant_code=row["货品编号"],
                merchant_name=row["品名"],
                price=row["固定成本价"],
                create_time=row["创建时间"],
                merchant_english=row["英文名"],
                category=row["品类"],
                season=row["季节"],
            )
            goods_list.append(goods)

        try:
            Goods.objects.all().delete()
            inserted_count = Goods.objects.bulk_create(goods_list)
            return JsonResponse({'message': f'{len(inserted_count)} 条数据更新成功。'})
        except DatabaseError as e:
            return JsonResponse({'error': str(e)}, status=500)


class UpdateSalesRecord(APIView):
    # 上传档口销量表
    def post(self, request):
        excel_file = request.data.get('excel-file')
        if not excel_file:
            return Response({'error': '文件未上传'}, status=400)

            # 处理Excel文件，提取数据或存储到数据库

        df = pd.read_excel(excel_file, header=0)
        df = df.astype(str)

        salesRecord_list = []
        for index, row in df.iterrows():
            if row["出库时间"] == 'nan':
                outgoing_time = None
            else:
                outgoing_time = pd.to_datetime(row["出库时间"])

            transaction_time = pd.to_datetime(row["交易时间"])

            salesRecord = SalesRecord(
                recipient=row["收货人"],
                product_code=row["货品编号"],
                product_name=row["品名"],
                specification=row["规格"],
                price=row["价格"],
                discount=row["折扣"],
                quantity=row["数量"],
                total=row["合计"],
                barcode=row["条码"],
                store=row["店铺"],
                transaction_time=transaction_time,
                outgoing_time=outgoing_time,
            )
            salesRecord_list.append(salesRecord)

        try:
            SalesRecord.objects.all().delete()
            inserted_count = SalesRecord.objects.bulk_create(salesRecord_list)
            return JsonResponse({'message': f'{len(inserted_count)} 条数据更新成功。'})
        except DatabaseError as e:
            return JsonResponse({'error': str(e)}, status=500)


class UpdateStock(APIView):
    # 上传库存表
    def post(self, request):
        excel_file = request.data.get('excel-file')
        if not excel_file:
            return Response({'error': '文件未上传'}, status=400)

            # 处理Excel文件，提取数据或存储到数据库
        df = pd.read_excel(excel_file, header=0)
        stock_summary = {}

        for index, row in df.iterrows():
            warehouse = row["仓库"]
            code = row["货品编号"]
            inventory = row["库存量"]
            order_quantity = row["订购量"]
            waiting_quantity = row["待发量"]
            orderable = row["可订购"]
            shippable = row["可发货"]
            number = row["总销量"]

            # 构建唯一的键，以货品编号和仓库作为键
            key = (code, warehouse)

            # 检查键是否存在于字典中，如果存在则更新对应的值，否则将其添加到字典中
            if key in stock_summary:
                stock_summary[key]["inventory"] += inventory
                stock_summary[key]["order_quantity"] += order_quantity
                stock_summary[key]["waiting_quantity"] += waiting_quantity
                stock_summary[key]["orderable"] += orderable
                stock_summary[key]["shippable"] += shippable
                stock_summary[key]["number"] += number
            else:
                stock_summary[key] = {
                    "inventory": inventory,
                    "order_quantity": order_quantity,
                    "waiting_quantity": waiting_quantity,
                    "orderable": orderable,
                    "shippable": shippable,
                    "number": number
                }

        stock_list = []

        # 根据字典中的数据构建 Stock 对象列表
        for key, values in stock_summary.items():
            stock = Stock(
                house=key[1],  # 仓库
                code=key[0],  # 货品编号
                inventory=values["inventory"],
                order_quantity=values["order_quantity"],
                waiting_quantity=values["waiting_quantity"],
                orderable=values["orderable"],
                shippable=values["shippable"],
                number=values["number"]
            )
            stock_list.append(stock)

        newstock_list = []

        for index, row in df.iterrows():
            if row['库存量'] == 0:
                continue
            else:
                stock = new_Stock(
                    house=row['仓库'],  # 仓库
                    code=row['货品编号'],  # 货品编号
                    cls=row['规格'],  # 货品编号
                    inventory=row['库存量'],
                    order_quantity=row['订购量'],
                    waiting_quantity=row['待发量'],
                    orderable=row['可订购'],
                    shippable=row['可发货']
                )
            newstock_list.append(stock)

        try:
            Stock.objects.all().delete()
            inserted_count1 = Stock.objects.bulk_create(stock_list)
            new_Stock.objects.all().delete()
            inserted_count2 = new_Stock.objects.bulk_create(newstock_list)
            return JsonResponse({'message': f'{len(inserted_count2)} 条数据更新成功。'})
        except DatabaseError as e:
            return JsonResponse({'error': str(e)}, status=500)


class UpdateStockIn(APIView):
    # 上传档口调拨表
    def post(self, request):
        excel_file = request.data.get('excel-file')
        if not excel_file:
            return Response({'error': '文件未上传'}, status=400)

            # 处理Excel文件，提取数据或存储到数据库
        df = pd.read_excel(excel_file, header=0)
        stock_list = []

        for index, row in df.iterrows():
            if row["入库原因"] == "调拨入库" or row["入库原因"] == "采购入库":
                stock = StockIn(
                    product_code=row['货品货号'],  # 仓库
                    product_name=row['货品名称'],  # 货品编号
                    specification=row['规格'],  # 货品编号
                    quantity=row['数量'],
                    reason=row['入库原因'],
                    handler=row['经办人'],
                    registration_time=row['登记时间'],
                )
                stock_list.append(stock)
            else:
                continue
        try:
            StockIn.objects.all().delete()
            inserted_count = StockIn.objects.bulk_create(stock_list)
            return JsonResponse({'message': f'{len(inserted_count)} 条数据更新成功。'})
        except DatabaseError as e:
            return JsonResponse({'error': str(e)}, status=500)


class UpdateCommodity(APIView):
    # 上传全量表
    def post(self, request):
        excel_file = request.data.get('excel-file')
        if not excel_file:
            return Response({'error': '文件未上传'}, status=400)

        # 处理Excel文件，提取数据或存储到数据库
        df = pd.read_excel(excel_file, header=0)
        commodity_list = []
        for index, row in df.iterrows():
            commodity = Commodity(
                commodity_image=row["商品图片"],
                commodity_title=row["商品标题"],
                commodity_code=row["商品编号"],
                deal_amount=row["成交金额"],
                settlement_amount=row["实际结算金额"],
                deal_refund_amount=row["成交退款率"],
                pre_shipment_refund_rate=row["发货前成交退款率"],
                post_shipment_refund_rate=row["发货后成交退款率"],
                live_exposure_count=row["直播间商品曝光人数"],
                live_click_count=row["直播间商品点击人数"],
                live_deal_amount=row["直播间成交金额"],
                live_deal_order_count=row["直播间成交订单数"],
                live_deal_item_count=row["直播间成交件数"],
                live_deal_user_count=row["直播间成交人数"],
                live_deal_conversion_rate=row["直播间成交转化率"],
                quality_return_rate=row["品质退货率（滞后）"],
                negative_review_rate=row["差评率"],
                positive_review_count=row["好评数"],
            )
            commodity_list.append(commodity)

        try:
            Commodity.objects.all().delete()
            inserted_count = Commodity.objects.bulk_create(commodity_list)
            return JsonResponse({'message': f'{len(inserted_count)} 条数据更新成功。'})
        except DatabaseError as e:
            return JsonResponse({'error': str(e)}, status=500)


class UpdateSize(APIView):
    # 上传尺寸表，并生成整合表
    def post(self, request):
        excel_file = request.data.get('excel-file')
        if not excel_file:
            return Response({'error': '文件未上传'}, status=400)

        # 处理Excel文件，提取数据或存储到数据库
        df = pd.read_excel(excel_file, header=0)
        size_list = []
        for index, row in df.iterrows():
            size = Size(
                code=row[0],
                size=row[1],

            )
            size_list.append(size)
        query = '''
                INSERT INTO taiwei_Integration
                (code,creation_date,size,season,cost,specification_sales,
                available_quantity,stall_sales,stall_price,order_price,category,
                first_registration_time,last_registration_time)
                (
                SELECT
                a.merchant_code as code,
                DATE(a.create_time) as creation_date,
                b.size,
                a.season,
                a.price as cost,
                d.specification_sales,
                d.available_quantity,
                c.quantity as stall_sales,
                c.price as stall_price,
                e.product_amount as order_price,
                a.category,
                f.first_registration_time,
                f.last_registration_time
                FROM
                (
                SELECT
                merchant_code,
                create_time,
                merchant_name,
                season,
                price,
                category
                FROM
                taiwei_goods
                ) as a
                LEFT JOIN
                (
                SELECT
                code,
                MAX(size) as size
                FROM 
                taiwei_size
                GROUP BY code
                ) as b
                ON a.merchant_code = b.code
                
                LEFT JOIN
                (
                SELECT
                MAX(product_code) as code,
                AVG(price) as price,
                SUM(quantity) as quantity
                FROM
                taiwei_salesrecord
                WHERE transaction_time >= CURDATE() - INTERVAL 30 DAY
                GROUP BY product_code
                ) as c
                ON a.merchant_code = c.code
                
                LEFT JOIN
                (
                SELECT
                code,
                SUM(inventory) - SUM(order_quantity) as available_quantity,
                (
                    SELECT GROUP_CONCAT(inventory SEPARATOR '  ') 
                    FROM (
                        SELECT CONCAT(cls, '-', SUM(inventory)-SUM(order_quantity)) AS inventory
                        FROM taiwei_newstock AS n
                        WHERE n.code = taiwei_newstock.code
                        GROUP BY code, cls		
                    ) AS subquery
                ) AS specification_sales
            FROM taiwei_newstock
            GROUP BY code
            ) as d
            ON a.merchant_code = d.code	
                
            LEFT JOIN
            (	
                SELECT code, product_amount
                    FROM (
                        SELECT LEFT(merchant_code, LENGTH(merchant_code)-1) AS code,
                                     product_amount,
                                     COUNT(*) AS occurrence,
                                     ROW_NUMBER() OVER (PARTITION BY LEFT(merchant_code, LENGTH(merchant_code)-1) ORDER BY COUNT(*) DESC) AS rn
                        FROM taiwei_orders
                        GROUP BY LEFT(merchant_code, LENGTH(merchant_code)-1), product_amount
                    ) subquery
                    WHERE rn = 1
                    ORDER BY code
                )
                as e 	
                ON a.merchant_code = e.code	
                LEFT JOIN 
                    (
                    SELECT
                    product_code as code,
                    DATE(MIN(registration_time)) as first_registration_time,
                    DATE(MAX(registration_time)) as last_registration_time
                    FROM
                    taiwei_stock_in
                    GROUP BY product_code
                    ) as f
                    on a.merchant_code = f.code
                )									
        '''

        try:
            with transaction.atomic():
                Integration.objects.all().delete()
                cursor = connection.cursor()
                cursor.execute(query)
                Size.objects.all().delete()
                inserted_count = Size.objects.bulk_create(size_list)
                return JsonResponse({'message': f'{len(inserted_count)} 条数据更新成功。'})
        except DatabaseError as e:
            return JsonResponse({'error': str(e)}, status=500)


class UpdateOneCommodity(APIView):
    # 上传每日全量表
    def post(self, request):
        excel_file = request.data.get('excel-file')
        if not excel_file:
            return Response({'error': '文件未上传'}, status=400)

        # 处理Excel文件，提取数据或存储到数据库
        df = pd.read_excel(excel_file, header=0)
        commodity_list = []
        date_time = datetime.now().strftime("%Y-%m-%d")
        for index, row in df.iterrows():
            print(row["日期"])
            if '日期' in row.index:
                date_time = row['日期']
                date_time = date_time.strftime("%Y-%m-%d")
            else:
                date_time = datetime.now().strftime("%Y-%m-%d")

            oneCommodity = OneCommodity(
                commodity_image=row["商品图片"],
                commodity_title=row["商品标题"],
                commodity_code=row["商品编号"],
                deal_amount=row["成交金额"],
                settlement_amount=row["实际结算金额"],
                deal_refund_amount=row["成交退款率"],
                pre_shipment_refund_rate=row["发货前成交退款率"],
                post_shipment_refund_rate=row["发货后成交退款率"],
                live_exposure_count=row["直播间商品曝光人数"],
                live_click_count=row["直播间商品点击人数"],
                live_deal_amount=row["直播间成交金额"],
                live_deal_order_count=row["直播间成交订单数"],
                live_deal_item_count=row["直播间成交件数"],
                live_deal_user_count=row["直播间成交人数"],
                live_deal_conversion_rate=row["直播间成交转化率"],
                date_time=date_time
            )
            commodity_list.append(oneCommodity)
        try:
            OneCommodity.objects.filter(date_time=date_time).delete()
            inserted_count = OneCommodity.objects.bulk_create(commodity_list)
            return JsonResponse({'message': f'{len(inserted_count)} 条数据更新成功。'})
        except DatabaseError as e:
            return JsonResponse({'error': str(e)}, status=500)


class UpdateMaterials(APIView):
    # 上传辅料表
    def post(self, request):
        excel_file = request.data.get('excel-file')
        if not excel_file:
            return Response({'error': '文件未上传'}, status=400)

        try:
            with pd.ExcelFile(excel_file) as xls:
                materials_list = []
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name, header=0)
                    if '日期' not in df.columns:
                        continue
                    for index, row in df.iterrows():
                        row = row.replace({' ': None, '/': None})
                        row = row.where(pd.notnull(row), None)
                        try:
                            date = (pd.to_datetime('1900-01-01') + pd.to_timedelta(row.iloc[0] - 2, 'D')).date()
                        except Exception as e:
                            date = pd.to_datetime(row[0], errors='coerce')
                            if pd.notnull(date):
                                date = date.strftime("%Y-%m-%d")
                            else:
                                continue
                        materials = Materials(
                            time=date,
                            merchant_code=row.iloc[1],
                            price=row.iloc[2],
                            remark=row.iloc[3]
                        )
                        materials_list.append(materials)

                try:
                    with transaction.atomic():
                        Materials.objects.all().delete()
                        inserted_count = Materials.objects.bulk_create(materials_list)
                    return JsonResponse({'message': f'{len(inserted_count)} 条数据更新成功。'})
                except DatabaseError as e:
                    return JsonResponse({'error': str(e)}, status=500)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class getUserInfo(APIView):
    # 获取商品的成功、退回、待发+在途的信息
    def get(self, request):
        name = request.query_params.get('name')
        search_date = request.query_params.get('search_date').split(',')
        start_time = '2000-01-01'
        end_time = '2100-01-01'
        if search_date[0] != 'null':
            start_time = search_date[0]
            end_time = search_date[1]
        query1 = '''
            SELECT NULL as id,u.name, o.merchant_code,c.commodity_image,
            SUBSTRING_INDEX(SUBSTRING_INDEX(o.product_name, '-', 2), '-', -1) AS product_name,
            REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(o.product_name, '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category,
			o.order_total_amount / o.product_quantity as price 
            FROM (`taiwei_user` AS u
            RIGHT JOIN taiwei_orders AS o ON u.sub_order_no = o.sub_order_no) LEFT JOIN taiwei_commodity as c ON o.product_id = c.commodity_code
            WHERE (o.order_status = '已完成' AND (o.after_sale_status LIKE '%%售后关闭%%' OR o.after_sale_status = '-'))
            AND u.`name` = %s
            AND DATE(o.order_submit_time) BETWEEN %s AND %s
        '''
        query2 = '''
            SELECT NULL as id,u.name, o.merchant_code,c.commodity_image,
            SUBSTRING_INDEX(SUBSTRING_INDEX(o.product_name, '-', 2), '-', -1) AS product_name,
            REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(o.product_name, '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category,
			o.order_total_amount / o.product_quantity as price 
            FROM (`taiwei_user` AS u
            RIGHT JOIN taiwei_orders AS o ON u.sub_order_no = o.sub_order_no) LEFT JOIN taiwei_commodity as c ON o.product_id = c.commodity_code
            WHERE (
                (o.order_status = '已关闭' AND (o.after_sale_status LIKE '%%退款成功%%' AND (o.merchant_remark LIKE '%%退货%%' OR o.merchant_remark LIKE '%%拒收%%' OR o.merchant_remark LIKE '%%退回%%')))
                OR (o.order_status = '已发货' AND (o.after_sale_status LIKE '%%售后待处理%%' OR o.after_sale_status LIKE '%%待收退货%%' OR o.after_sale_status LIKE '%%待退货%%' OR o.after_sale_status LIKE '%%退款成功%%'))
                OR (o.order_status = '已完成' AND (o.after_sale_status LIKE '%%待收退货%%' OR o.after_sale_status LIKE '%%待退货%%' OR o.after_sale_status LIKE '%%退款成功%%'))
            )
            AND u.`name` = %s
            AND DATE(o.order_submit_time) BETWEEN %s AND %s
        '''
        query3 = '''
            SELECT NULL as id,u.name, o.merchant_code,c.commodity_image,
            SUBSTRING_INDEX(SUBSTRING_INDEX(o.product_name, '-', 2), '-', -1) AS product_name,
            REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(o.product_name, '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category,
			o.order_total_amount / o.product_quantity as price 
            FROM (`taiwei_user` AS u
            RIGHT JOIN taiwei_orders AS o ON u.sub_order_no = o.sub_order_no) LEFT JOIN taiwei_commodity as c ON o.product_id = c.commodity_code
            WHERE ((o.order_status = '已发货' AND (o.after_sale_status LIKE '%%售后关闭%%' OR o.after_sale_status = '-'))
            OR (o.order_status = '待发货' AND o.after_sale_status = '-'))
            AND u.`name` = %s
            AND DATE(o.order_submit_time) BETWEEN %s AND %s
        '''
        user_info_query1 = User.objects.raw(query1, [name, start_time, end_time])
        user_info_query2 = User.objects.raw(query2, [name, start_time, end_time])
        user_info_query3 = User.objects.raw(query3, [name, start_time, end_time])

        serializer1 = UserInfoSerializer(user_info_query1, many=True)
        serializer2 = UserInfoSerializer(user_info_query2, many=True)
        serializer3 = UserInfoSerializer(user_info_query3, many=True)

        data = {
            'query1_results': serializer1.data,
            'query2_results': serializer2.data,
            'query3_results': serializer3.data,
        }

        return Response(data)


class getCodeInfo(APIView):
    # 获取商品的待发、取消、在途成功、退回的信息
    def get(self, request, submit_time):
        query1 = '''
                SELECT NULL as id,LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) as code,MAX(c.commodity_image) as commodity_image,
           MAX(REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(o.product_name, '】', -1), '-', 1), '[a-zA-Z0-9]', '')) AS category,
           SUM(o.product_quantity) as product_quantity
           FROM taiwei_orders as o
           LEFT JOIN taiwei_commodity as c ON o.product_id = c.commodity_code
           WHERE 
            order_status = '待发货' 
            AND after_sale_status = '-'
            AND DATE(order_submit_time) = %s
           GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)    
                '''
        query2 = '''
                SELECT NULL as id,LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) as code,MAX(c.commodity_image) as commodity_image,
           MAX(REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(o.product_name, '】', -1), '-', 1), '[a-zA-Z0-9]', '')) AS category,
           SUM(o.product_quantity) as product_quantity
           FROM taiwei_orders as o
           LEFT JOIN taiwei_commodity as c ON o.product_id = c.commodity_code
           WHERE 
           (order_status = '已关闭' AND (after_sale_status like '%%退款成功%%' AND (merchant_remark LIKE '%%取消%%' OR merchant_remark='nan')))                
           AND DATE(order_submit_time) = %s
           GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)    
                '''
        query3 = '''
                SELECT NULL as id,LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) as code,MAX(c.commodity_image) as commodity_image,
           MAX(REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(o.product_name, '】', -1), '-', 1), '[a-zA-Z0-9]', '')) AS category,
           SUM(o.product_quantity) as product_quantity
           FROM taiwei_orders as o
           LEFT JOIN taiwei_commodity as c ON o.product_id = c.commodity_code
           WHERE 
           (order_status = '已发货' AND (after_sale_status LIKE '%%售后关闭%%' OR after_sale_status = '-'))
           AND DATE(order_submit_time) = %s
           GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)                    
                '''
        query4 = '''
                SELECT NULL as id,LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) as code,MAX(c.commodity_image) as commodity_image,
           MAX(REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(o.product_name, '】', -1), '-', 1), '[a-zA-Z0-9]', '')) AS category,
           SUM(o.product_quantity) as product_quantity
           FROM taiwei_orders as o
           LEFT JOIN taiwei_commodity as c ON o.product_id = c.commodity_code
           WHERE 
           (order_status = '已完成' AND (after_sale_status LIKE '%%售后关闭%%' OR after_sale_status = '-'))
           AND DATE(order_submit_time) = %s            
           GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)    
                '''
        query5 = '''
                SELECT NULL as id,LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) as code,MAX(c.commodity_image) as commodity_image,
           MAX(REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(o.product_name, '】', -1), '-', 1), '[a-zA-Z0-9]', '')) AS category,
           SUM(o.product_quantity) as product_quantity
           FROM taiwei_orders as o
           LEFT JOIN taiwei_commodity as c ON o.product_id = c.commodity_code
           WHERE 
           ((order_status = '已关闭' AND (after_sale_status LIKE '%%退款成功%%' 
                AND (merchant_remark LIKE '%%退货%%'
                OR merchant_remark LIKE '%%拒收%%'
                OR merchant_remark LIKE '%%退回%%')))
                OR (order_status = '已发货' AND 
                (after_sale_status LIKE '%%售后待处理%%' 
                OR after_sale_status LIKE '%%待收退货%%' 
                OR after_sale_status LIKE '%%待退货%%' 
                OR after_sale_status LIKE '%%退款成功%%' ))
                OR (order_status='已完成' AND 
                (after_sale_status LIKE '%%待收退货%%' 
                OR after_sale_status LIKE '%%待退货%%' 
                OR after_sale_status LIKE '%%退款成功%%')))
                AND DATE(order_submit_time) = %s
                GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)
                '''

        user_info_query1 = User.objects.raw(query1, [submit_time])
        user_info_query2 = User.objects.raw(query2, [submit_time])
        user_info_query3 = User.objects.raw(query3, [submit_time])
        user_info_query4 = User.objects.raw(query4, [submit_time])
        user_info_query5 = User.objects.raw(query5, [submit_time])

        serializer1 = CodeInfoSerializer(user_info_query1, many=True)
        serializer2 = CodeInfoSerializer(user_info_query2, many=True)
        serializer3 = CodeInfoSerializer(user_info_query3, many=True)
        serializer4 = CodeInfoSerializer(user_info_query4, many=True)
        serializer5 = CodeInfoSerializer(user_info_query5, many=True)

        data = {
            'query1_results': serializer1.data,
            'query2_results': serializer2.data,
            'query3_results': serializer3.data,
            'query4_results': serializer4.data,
            'query5_results': serializer5.data,
        }

        return Response(data)


class getReportList(ListAPIView):
    serializer_class = ReportSerializer
    pagination_class = OrderPagination

    # 获取每日报表
    def get_queryset(self):

        submit_time = datetime.now().strftime("%Y-%m-%d")
        search_submit_time = self.request.GET.get('report_data')
        # 哪一天的报表
        search_submit_time_history = self.request.GET.get('report_data_history')
        if search_submit_time:
            submit_time = datetime.strptime(search_submit_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            previous_day = submit_time + timedelta(days=1)
            submit_time = previous_day.strftime("%Y-%m-%d")

        if search_submit_time_history:
            submit_time = datetime.strptime(search_submit_time_history, "%Y-%m-%dT%H:%M:%S.%fZ")
            previous_day = submit_time + timedelta(days=1)
            submit_time = previous_day.strftime("%Y-%m-%d")
            queryset = Report.objects.filter(order_submit_time=submit_time)

            return queryset

        queryset = Report.objects.filter(data_time=submit_time).order_by('-order_submit_time')

        return queryset


class OrderTrackingView(APIView):
    def post(self, request):
        """
        根据款号添加要追踪的款号
        :param request:
        :return:
        """
        code = request.data.get('code')
        query = '''
            INSERT INTO 
            taiwei_tracking 
            (code,name, image, order_quantity, 
            cutting_quantity, workshop_quantity, 
            rear_quantity, taiwei_quantity, 
            yifa_quantity,moya_quantity, live_exposure_count, 
            live_deal_item_count, 
            cancelled_quantity, pending_shipment_quantity,
             successful_quantity, returned_quantity)
            SELECT 
                MAX(s.code),
                MAX(r.category),
                MAX(g.commodity_image),
                MAX(s.inventory),
                MAX(s.order_quantity_cutting),
                MAX(s.order_quantity_workshop),
                MAX(s.order_quantity_rear),
                MAX(s.order_quantity_taiwei),
                MAX(s.order_quantity_yifa),
                MAX(s.order_quantity_moya),
                MAX(g.live_exposure_count),
                MAX(g.live_deal_item_count),
                MAX(r.cancelled),
                MAX(r.pending_shipment),
                MAX(r.successful),
                MAX(r.returned)
            FROM (
                SELECT 
                    code,
                    SUM(order_quantity) AS inventory,
                    SUM(CASE WHEN house LIKE '裁床%%' THEN inventory ELSE 0 END) AS order_quantity_cutting,
                    SUM(CASE WHEN house LIKE '%%车间%%' THEN inventory ELSE 0 END) AS order_quantity_workshop,
                    SUM(CASE WHEN house LIKE '后道%%' THEN inventory ELSE 0 END) AS order_quantity_rear,
                    SUM(CASE WHEN house = '泰维仓' THEN inventory ELSE 0 END) AS order_quantity_taiwei,
                    SUM(CASE WHEN house LIKE '意法%%' THEN inventory ELSE 0 END) AS order_quantity_yifa,
                    SUM(CASE WHEN house LIKE '茉雅%%' THEN inventory ELSE 0 END) AS order_quantity_moya
                FROM taiwei_stock
                WHERE code = %s 
                GROUP BY code
            ) AS s
            LEFT JOIN (
                SELECT 
                    LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) as code,
                    MAX(c.commodity_image) as commodity_image,
                    MAX(c.live_exposure_count) as live_exposure_count,
                    MAX(c.live_deal_item_count) as live_deal_item_count
                FROM taiwei_orders AS o 
                LEFT JOIN taiwei_commodity AS c 
                ON o.product_id = c.commodity_code
                WHERE LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) = %s
                GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)
            ) AS g ON s.code = g.code
            LEFT JOIN (
                SELECT 
                    LEFT(merchant_code, LENGTH(merchant_code) - 1) as code,
                    SUM(product_quantity) AS cancelled,
                    0 AS pending_shipment,
                    0 AS successful,
                    0 AS returned,
                    REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
                FROM taiwei_orders 
                WHERE (order_status = '已关闭' AND 
                (after_sale_status like '%%退款成功%%' AND 
                (merchant_remark LIKE '%%取消%%' OR merchant_remark='nan'))) 
                AND LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s 
                GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)
            
                UNION ALL
            
                SELECT 
                    LEFT(merchant_code, LENGTH(merchant_code) - 1) as code,
                    0 AS cancelled,
                    SUM(product_quantity) AS pending_shipment,
                    0 AS successful,
                    0 AS returned,
                    NULL as category
                FROM `taiwei_orders`  
                WHERE ((order_status = '已发货' AND 
                (after_sale_status LIKE '%%售后关闭%%' OR after_sale_status = '-')) 
                OR (order_status = '待发货' AND after_sale_status = '-'))
                AND LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s 
                GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)
            
                UNION ALL
            
                SELECT 
                    LEFT(merchant_code, LENGTH(merchant_code) - 1) as code,
                    0 AS cancelled,
                    0 AS pending_shipment,
                    SUM(product_quantity) AS successful,
                    0 AS returned,
                    NULL as category
                FROM `taiwei_orders`  
                WHERE (order_status = '已完成' AND 
                (after_sale_status LIKE '%%售后关闭%%' OR after_sale_status = '-'))  
                AND LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s 
                GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)
            
                UNION ALL
            
                SELECT
                    LEFT(merchant_code, LENGTH(merchant_code) - 1) as code,
                    0 AS cancelled,
                    0 AS pending_shipment,
                    0 AS successful,
                    SUM(product_quantity) AS returned,
                    NULL as category
                FROM `taiwei_orders`  
                WHERE ((order_status = '已关闭' 
                AND (after_sale_status LIKE '%%退款成功%%' 
                AND (merchant_remark LIKE '%%退货%%' 
                OR merchant_remark LIKE '%%拒收%%' 
                OR merchant_remark LIKE '%%退回%%'))) 
                OR (order_status = '已发货' 
                AND (after_sale_status LIKE '%%售后待处理%%' 
                OR after_sale_status LIKE '%%待收退货%%' 
                OR after_sale_status LIKE '%%待退货%%' 
                OR after_sale_status LIKE '%%退款成功%%' )) 
                OR (order_status='已完成' 
                AND (after_sale_status LIKE '%%待收退货%%' 
                OR after_sale_status LIKE '%%待退货%%' 
                OR after_sale_status LIKE '%%退款成功%%'))) 
                AND LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s
                GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)
            ) AS r ON s.code = r.code
            GROUP BY s.code
        '''

        with connection.cursor() as cursor:
            cursor.execute(query, [code, code, code, code, code, code])
        return HttpResponse("OK")

    def get(self, request):
        # 获取所有的追踪的款号信息
        queryset = OrderTracking.objects.all()
        serializer = OrderTrackingSerializer(queryset, many=True)
        return Response(serializer.data)

    def delete(self, request):
        # 删除不需要追踪的款号
        id = request.query_params.get('id')
        OrderTracking.objects.get(pk=id).delete()
        return HttpResponse("ok")

    def patch(self, request):
        # 当订单发生变化就需要重新生成该款号追踪内容的详细信息（刷新）
        code_list = request.data.get('code_list')
        OrderTracking.objects.filter(code__in=code_list).delete()
        query = '''
                    INSERT INTO 
                    taiwei_tracking 
                    (code,name, image, order_quantity, 
                    cutting_quantity, workshop_quantity, 
                    rear_quantity, taiwei_quantity, 
                    yifa_quantity,moya_quantity, live_exposure_count, 
                    live_deal_item_count, 
                    cancelled_quantity, pending_shipment_quantity,
                     successful_quantity, returned_quantity)
                    SELECT 
                        MAX(s.code),
                        MAX(r.category),
                        MAX(g.commodity_image),
                        MAX(s.inventory),
                        MAX(s.order_quantity_cutting),
                        MAX(s.order_quantity_workshop),
                        MAX(s.order_quantity_rear),
                        MAX(s.order_quantity_taiwei),
                        MAX(s.order_quantity_yifa),
                        MAX(s.order_quantity_moya),
                        MAX(g.live_exposure_count),
                        MAX(g.live_deal_item_count),
                        MAX(r.cancelled),
                        MAX(r.pending_shipment),
                        MAX(r.successful),
                        MAX(r.returned)
                    FROM (
                        SELECT 
                            code,
                            SUM(order_quantity) AS inventory,
                            SUM(CASE WHEN house LIKE '裁床%%' THEN inventory ELSE 0 END) AS order_quantity_cutting,
                            SUM(CASE WHEN house LIKE '%%车间%%' THEN inventory ELSE 0 END) AS order_quantity_workshop,
                            SUM(CASE WHEN house LIKE '后道%%' THEN inventory ELSE 0 END) AS order_quantity_rear,
                            SUM(CASE WHEN house = '泰维仓' THEN inventory ELSE 0 END) AS order_quantity_taiwei,
                            SUM(CASE WHEN house LIKE '意法%%' THEN inventory ELSE 0 END) AS order_quantity_yifa,
                            SUM(CASE WHEN house LIKE '茉雅%%' THEN inventory ELSE 0 END) AS order_quantity_moya
                        FROM taiwei_stock
                        WHERE code = %s 
                        GROUP BY code
                    ) AS s
                    LEFT JOIN (
                        SELECT 
                            LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) as code,
                            MAX(c.commodity_image) as commodity_image,
                            MAX(c.live_exposure_count) as live_exposure_count,
                            MAX(c.live_deal_item_count) as live_deal_item_count
                        FROM taiwei_orders AS o 
                        LEFT JOIN taiwei_commodity AS c 
                        ON o.product_id = c.commodity_code
                        WHERE LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) = %s
                        GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)
                    ) AS g ON s.code = g.code
                    LEFT JOIN (
                        SELECT 
                            LEFT(merchant_code, LENGTH(merchant_code) - 1) as code,
                            SUM(product_quantity) AS cancelled,
                            0 AS pending_shipment,
                            0 AS successful,
                            0 AS returned,
                            REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
                        FROM taiwei_orders 
                        WHERE (order_status = '已关闭' AND 
                        (after_sale_status like '%%退款成功%%' AND 
                        (merchant_remark LIKE '%%取消%%' OR merchant_remark='nan'))) 
                        AND LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s 
                        GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)

                        UNION ALL

                        SELECT 
                            LEFT(merchant_code, LENGTH(merchant_code) - 1) as code,
                            0 AS cancelled,
                            SUM(product_quantity) AS pending_shipment,
                            0 AS successful,
                            0 AS returned,
                            NULL as category
                        FROM `taiwei_orders`  
                        WHERE ((order_status = '已发货' AND 
                        (after_sale_status LIKE '%%售后关闭%%' OR after_sale_status = '-')) 
                        OR (order_status = '待发货' AND after_sale_status = '-'))
                        AND LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s 
                        GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)

                        UNION ALL

                        SELECT 
                            LEFT(merchant_code, LENGTH(merchant_code) - 1) as code,
                            0 AS cancelled,
                            0 AS pending_shipment,
                            SUM(product_quantity) AS successful,
                            0 AS returned,
                            NULL as category
                        FROM `taiwei_orders`  
                        WHERE (order_status = '已完成' AND 
                        (after_sale_status LIKE '%%售后关闭%%' OR after_sale_status = '-'))  
                        AND LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s 
                        GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)

                        UNION ALL

                        SELECT
                            LEFT(merchant_code, LENGTH(merchant_code) - 1) as code,
                            0 AS cancelled,
                            0 AS pending_shipment,
                            0 AS successful,
                            SUM(product_quantity) AS returned,
                            NULL as category
                        FROM `taiwei_orders`  
                        WHERE ((order_status = '已关闭' 
                        AND (after_sale_status LIKE '%%退款成功%%' 
                        AND (merchant_remark LIKE '%%退货%%' 
                        OR merchant_remark LIKE '%%拒收%%' 
                        OR merchant_remark LIKE '%%退回%%'))) 
                        OR (order_status = '已发货' 
                        AND (after_sale_status LIKE '%%售后待处理%%' 
                        OR after_sale_status LIKE '%%待收退货%%' 
                        OR after_sale_status LIKE '%%待退货%%' 
                        OR after_sale_status LIKE '%%退款成功%%' )) 
                        OR (order_status='已完成' 
                        AND (after_sale_status LIKE '%%待收退货%%' 
                        OR after_sale_status LIKE '%%待退货%%' 
                        OR after_sale_status LIKE '%%退款成功%%'))) 
                        AND LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s
                        GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)
                    ) AS r ON s.code = r.code
                    GROUP BY s.code
                '''

        with connection.cursor() as cursor:
            for code in code_list:
                cursor.execute(query, [code, code, code, code, code, code])
        return HttpResponse("ok")


class UpdateStatusView(APIView):
    """
    用于查询和修改，上传数据的最后日期
    """

    def get(self, request):
        queryset = UpdateStatus.objects.all()
        serializer = UpdateStatusSerializer(queryset, many=True)
        return Response(serializer.data)

    # 修改某一个表格的最后上传日期
    def put(self, request):
        id = request.data.get('id')
        day = datetime.now().strftime('%d')
        UpdateStatus.objects.filter(pk=id).update(date_time=day)

        return Response("OK")


class VipUserView(APIView):
    """
    用于添加和获取vip用户的名单
    """

    def post(self, request):
        # 添加vip用户
        name = request.data.get('name')
        VipUser.objects.create(name=name)  # 创建VipUser对象并保存到数据库
        return Response("OK")

    def get(self, request):
        # 查询出所有的VIP用户
        # original_data为用户全称 modified_data为用户的用户名称前四个字符
        queryset = VipUser.objects.all()  # 获取所有VipUser对象
        serializer1 = VipUserSerializer(queryset, many=True)  # 序列化所有VipUser对象

        modified_data = serializer1.data.copy()  # 复制一份原始数据，用于修改
        for item in modified_data:
            item['name'] = item['name'][:4]  # 修改每个对象的'name'字段为前四个字符

        serializer2 = VipUserSerializer(queryset, many=True)  # 使用原始的未修改数据创建序列化器

        response_data = {
            'modified_data': modified_data,  # 修改后的数据
            'original_data': serializer2.data  # 原始数据
        }

        return Response(response_data, status=status.HTTP_200_OK)

    def delete(self, request):
        # 根据用户名删除VIP用户
        name = request.query_params.get('name')  # 获取查询参数中的'name'值
        VipUser.objects.filter(name=name).delete()  # 根据'name'值过滤并删除对应的VipUser对象
        return HttpResponse("ok")


class SearchCodeView(APIView):
    # 全量表款号跟踪
    # 查询出 传入的每日全量表的日期开始 对应的每天全量表该款号的信息
    def get(self, request):
        # 款号
        code = request.query_params.get('code') + '%'
        # 每日全量表开始日期
        data_time = request.query_params.get('data_time')
        # 查询出全量表的销量、曝光量、点击率、点击成交率件数、成功件数、待发件数、在途件数、退回件数、千川订单成功件数
        query = """
            SELECT
                a.date_time,
                MAX(b.code) as code,
                SUM(a.live_deal_item_count) as live_deal_item_count,
                SUM(a.live_exposure_count) as live_exposure_count,
                SUM(a.live_click_count) as live_click_count,
                SUM(a.live_deal_user_count) as live_deal_user_count,
                SUM(b.success_num) as success_num,
                SUM(b.pending_num) as pending_num,
                SUM(b.transit_num) as transit_num,
                SUM(b.back_num) as back_num,
                SUM(b.liev_success_num) as liev_success_num
                FROM
                (
                SELECT
                date_time,
                SUM(live_deal_item_count) as live_deal_item_count,
                SUM(live_exposure_count) as live_exposure_count,
                SUM(live_click_count) / (CASE WHEN SUM(live_exposure_count)=0 THEN NULL ELSE SUM(live_exposure_count) END) as live_click_count,
                SUM(live_deal_user_count) / (CASE WHEN SUM(live_click_count)=0 THEN NULL ELSE SUM(live_click_count) END) as live_deal_user_count
                FROM
                taiwei_onecommodity
                WHERE date_time >= %s
                AND commodity_code IN (SELECT product_id FROM taiwei_orders WHERE merchant_code LIKE %s)
                GROUP BY date_time
                ) as a
                LEFT JOIN
                (
                SELECT
                MAX(code) as code,
                MAX(success_num) as success_num,
                MAX(pending_num) as pending_num,
                MAX(transit_num) as transit_num,
                MAX(back_num) as back_num, 
                MAX(liev_success_num) as liev_success_num,
                MAX(order_submit_time) as order_submit_time
                FROM
                (
                # 成功
                SELECT
                LEFT(MAX(merchant_code), LENGTH(MAX(merchant_code)) - 1) as code,
                SUM(product_quantity) as success_num,
                NULL as pending_num,
                NULL as transit_num,
                NULL as back_num,
                NULL as liev_success_num,
                DATE(order_submit_time) as order_submit_time
                FROM
                taiwei_orders
                WHERE
                (order_status = '已完成' AND (after_sale_status LIKE '%%售后关闭%%' OR after_sale_status = '-'))
                AND DATE(order_submit_time) >= %s
                AND merchant_code LIKE %s
                GROUP BY DATE(order_submit_time)
                UNION ALL
                # 待发
                SELECT
                LEFT(MAX(merchant_code), LENGTH(MAX(merchant_code)) - 1) as code,
                NULL as success_num,
                SUM(product_quantity) as pending_num,
                NULL as transit_num,
                NULL as back_num,
                NULL as liev_success_num,
                DATE(order_submit_time) as order_submit_time
                FROM
                taiwei_orders
                WHERE
                (order_status = '待发货'AND after_sale_status = '-')
                AND DATE(order_submit_time) >= %s
                AND merchant_code LIKE %s
                GROUP BY DATE(order_submit_time)
                
                UNION ALL
                # 在途
                SELECT
                LEFT(MAX(merchant_code), LENGTH(MAX(merchant_code)) - 1) as code,
                NULL as success_num,
                NULL as pending_num,
                SUM(product_quantity) as transit_num,
                NULL as back_num,
                NULL as liev_success_num,	
                DATE(order_submit_time) as order_submit_time
                FROM
                taiwei_orders
                WHERE
                (order_status = '已发货' AND (after_sale_status = '-' OR after_sale_status LIKE '%%售后关闭'))
                AND DATE(order_submit_time) >= %s
                AND merchant_code LIKE %s
                GROUP BY DATE(order_submit_time)
                        
                UNION ALL		
                #退回
                SELECT
                LEFT(MAX(merchant_code), LENGTH(MAX(merchant_code)) - 1) as code,
                NULL as success_num,
                NULL as pending_num,
                NULL as transit_num,
                SUM(product_quantity) as back_num,
                NULL as liev_success_num,
                DATE(order_submit_time) as order_submit_time
                    FROM
                            taiwei_orders
                    WHERE
                            (
                                    (order_status = '已关闭'
                                            AND (after_sale_status LIKE '%%退款成功%%'
                                                    AND (merchant_remark LIKE '%%退货%%'
                                                            OR merchant_remark LIKE '%%拒收%%'
                                                            OR merchant_remark LIKE '%%退回%%')
                                                    )
                                    )
                                    OR (order_status = '已发货'
                                            AND (after_sale_status LIKE '%%售后待处理%%'
                                                    OR after_sale_status LIKE '%%待收退货%%'
                                                    OR after_sale_status LIKE '%%待退货%%'
                                                    OR after_sale_status LIKE '%%退款成功%%')
                                            )
                                    OR (order_status = '已完成'
                                            AND (after_sale_status LIKE '%%待收退货%%'
                                                    OR after_sale_status LIKE '%%待退货%%'
                                                    OR after_sale_status LIKE '%%退款成功%%')
                                            )
                            )
                            AND DATE(order_submit_time) >= %s
                            AND merchant_code LIKE %s
                    GROUP BY DATE(order_submit_time)
                
                UNION ALL
                
                # 千川成功
                SELECT
                LEFT(MAX(merchant_code), LENGTH(MAX(merchant_code)) - 1) as code,
                NULL as success_num,
                NULL as pending_num,
                NULL as transit_num,
                NULL as back_num,
                SUM(product_quantity) as liev_success_num,
                DATE(order_submit_time) as order_submit_time
                FROM
                taiwei_orders
                WHERE
                (order_status = '已完成' AND (after_sale_status LIKE '%%售后关闭%%' OR after_sale_status = '-'))
                AND ad_channel = '直播'
                AND DATE(order_submit_time) >= %s
                AND merchant_code LIKE %s
                GROUP BY DATE(order_submit_time)
                ) as o
                GROUP BY order_submit_time
            )as b
            ON  a.date_time = b.order_submit_time
            GROUP BY a.date_time 
       """
        # 查询出该款号的库存、订购量、待退货件数、待收退货件数
        query2 = """
            SELECT
            *
            FROM
            (
            SELECT
            LEFT(merchant_code,LENGTH(merchant_code)-1) as code,
            SUM(CASE WHEN after_sale_status LIKE '%%待退货%%' THEN product_quantity ELSE 0 END) AS back_num,
            SUM(CASE WHEN after_sale_status LIKE '%%待收退货%%' THEN product_quantity ELSE 0 END) AS back_num2
            FROM
            taiwei_orders
            WHERE
            merchant_code LIKE %s
            GROUP BY LEFT(merchant_code,LENGTH(merchant_code)-1)
            ) as a
            LEFT JOIN
            (
            SELECT
            code,
            SUM(inventory) as inventory,
            SUM(order_quantity) as order_quantity
            FROM 
            taiwei_stock
            WHERE (house = '泰维仓' OR house LIKE '意法%%'  OR house LIKE '茉雅%%')
            AND code LIKE %s
            GROUP BY code
            ) as b
            ON a.code = b.code
        """
        # 查询出该款号的裁床库存、车间库存、后道库存
        query3 = """
            SELECT
            code,
            SUM(CASE WHEN house LIKE '%%裁床%%' THEN inventory ELSE 0 END) as cai_chuang,
            SUM(CASE WHEN house LIKE '%%车间%%' THEN inventory ELSE 0 END) as che_jian,
            SUM(CASE WHEN house LIKE '%%后道%%' THEN inventory ELSE 0 END) as hou_dao
            FROM
            taiwei_stock
            WHERE code LIKE %s
            GROUP BY `code`
        """

        with connection.cursor() as cursor:
            cursor.execute(query, [data_time, code, data_time, code, data_time, code, data_time, code,
                                   data_time, code, data_time, code])
            result = cursor.fetchall()
            cursor.execute(query2, [code, code])
            result2 = cursor.fetchall()
            cursor.execute(query3, [code])
            result3 = cursor.fetchall()
        return Response({'status': 'success', 'message': {"data1": result, 'data2': result2, 'data3': result3}},
                        status=200)


class updateRepeatOrder(APIView):
    # 上传下单简报
    def post(self, request):
        excel_file = request.data.get('excel-file')
        if not excel_file:
            return Response({'error': '文件未上传'}, status=400)

            # 处理Excel文件，提取数据或存储到数据库
        # 开启事务
        with transaction.atomic():
            # 只要sheet_name为新款和翻单的表格
            df1 = pd.read_excel(excel_file, sheet_name='新款', header=0)
            df2 = pd.read_excel(excel_file, sheet_name='翻单', header=0)
            newStyle_list = []
            repeatOrder_list = []
            # 计算出当前的日期
            date_time = datetime.now().strftime("%Y-%m-%d")
            date_time = datetime.strptime(date_time, "%Y-%m-%d")
            StyleStatus.objects.filter(date_time=date_time).delete()
            for index, row in df1.iterrows():
                if str(row.iloc[6]).strip().__len__() == 0 or pd.isnull(row.iloc[6]):  # 检查 总件数 是否为空
                    row.iloc[6] = 100
                row = row.replace({' ': None, '/': None})
                row = row.where(pd.notnull(row), None)
                if pd.isnull(row.iloc[0]):  # 检查 row.iloc[0] 是否为空
                    continue  # 如果为空，则跳过当前迭代并进入下一次迭代
                # 转换成下单简报的模型类
                new_style = newStyle(
                    date=row.iloc[0] or None,
                    code=row.iloc[2] or None,
                    designer=row.iloc[3] or None,
                    number_of_pieces=row.iloc[5] or None,
                    total_number_of_pieces=row.iloc[6] or None,
                    order_maker=row.iloc[7] or None,
                    confirmation_on_the_day=row.iloc[9] or None,
                    fabric_arrival_time=row.iloc[10] or None,
                    circulation_table_flow_down_time=row.iloc[11] or None,
                    material_fill_craft_package_material_post_road=row.iloc[12] or None,
                    category=row.iloc[15] or None,
                )

                newStyle_list.append(new_style)
                status_time_timestamp = row.iloc[0]
                status_time = status_time_timestamp.to_pydatetime()
                # target_date = datetime(2023, 6, 2)
                # try:
                #     if status_time > target_date:
                #         insert_new_style_status_tracking(status_time, row.iloc[6], '新款', row.iloc[2])
                # except Exception as e:
                #     return JsonResponse({'error': str(e)}, status=500)
                try:
                    # 调用insert_style_status把该条内容插入数据库

                    insert_style_status(status_time, date_time, '新款', row.iloc[2])
                    if not NewStyleStatusTracking.objects.filter(code=row.iloc[2]).exists():
                        insert_new_style_status_tracking(status_time, row.iloc[6], '新款', row.iloc[2])

                except DatabaseError as e:
                    return JsonResponse({'error': str(e)}, status=500)

            for index, row in df2.iterrows():
                if str(row.iloc[6]).strip().__len__() == 0 or pd.isnull(row.iloc[6]):  # 检查 总件数 是否为空
                    row.iloc[6] = 100
                if pd.isnull(row.iloc[0]):  # 检查 row.iloc[0] 是否为空
                    continue  # 如果为空，则跳过当前迭代并进入下一次迭代
                row = row.replace({' ': None, '/': None})
                row = row.where(pd.notnull(row), None)
                repeat_order = repeatOrder(
                    date=row.iloc[0] or None,
                    code=row.iloc[2] or None,
                    number_of_pieces=row.iloc[5] or None,
                    total_number_of_pieces=row.iloc[6] or None,
                    circulation=row.iloc[7] or None,
                    daily_status=row.iloc[8] or None,
                    fabric_arrival_time=row.iloc[10] or None,
                    circulation_table_flow_down=row.iloc[12] or None,
                )
                repeatOrder_list.append(repeat_order)
                status_time_timestamp = row.iloc[0]
                status_time = status_time_timestamp.to_pydatetime()
                # target_date = datetime(2023, 6, 2)
                # try:
                #     if status_time > target_date:
                #         insert_new_style_status_tracking(status_time, row.iloc[6], '翻单', row.iloc[2])
                # except Exception as e:
                #     return JsonResponse({'error': str(e)}, status=500)
                try:
                    insert_style_status(status_time, date_time, '翻单', row.iloc[2])
                    if not NewStyleStatusTracking.objects.filter(code=row.iloc[2], status="翻单",
                                                                 order_date=row.iloc[0]).exists():
                        insert_new_style_status_tracking(status_time, row.iloc[6], '翻单', row.iloc[2])
                except DatabaseError as e:
                    return JsonResponse({'error': str(e)}, status=500)

            try:
                newStyle.objects.all().delete()
                repeatOrder.objects.all().delete()
                inserted_count = newStyle.objects.bulk_create(newStyle_list)
                inserted_count2 = repeatOrder.objects.bulk_create(repeatOrder_list)
                return JsonResponse({'message': f'{len(inserted_count)} 条数据更新成功。'})
            except DatabaseError as e:
                return JsonResponse({'error': str(e)}, status=500)


class updateFabric(APIView):
    # 上传面料表
    # 功能和工厂表
    def post(self, request):
        excel_file = request.data.get('excel-file')
        if not excel_file:
            return Response({'error': '文件未上传'}, status=400)
        try:
            with pd.ExcelFile(excel_file) as xls:
                fabric_list = []
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name, header=0)
                    if '日期' not in df.columns:
                        continue
                    for index, row in df.iterrows():
                        row = row.replace({' ': None, '/': None})
                        row = row.where(pd.notnull(row), None)
                        if row.iloc[0] is None:
                            continue
                        try:
                            date = (pd.to_datetime('1900-01-01') + pd.to_timedelta(row.iloc[0] - 2, 'D')).date()
                        except Exception as e:
                            date = pd.to_datetime(row[0], errors='coerce')
                            if pd.notnull(date):
                                date = date.strftime("%Y-%m-%d")
                            else:
                                continue
                        fabric = Fabric(
                            time=date,
                            merchant_code=row.iloc[1],
                            price=row.iloc[2],
                            channel=row.iloc[3],
                            role=row.iloc[4],
                        )
                        fabric_list.append(fabric)
                with transaction.atomic():
                    Fabric.objects.all().delete()
                    inserted_count = Fabric.objects.bulk_create(fabric_list)
                    return JsonResponse({'message': f'{len(inserted_count)} 条数据更新成功。'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class updateFactory(APIView):
    # 上传工厂表
    def post(self, request):
        excel_file = request.data.get('excel-file')
        if not excel_file:
            return Response({'error': '文件未上传'}, status=400)
        try:
            # 表excel根据特定的密码进行解密
            file = msoffcrypto.OfficeFile(excel_file)
            file.load_key(password='095411')

            output_file = io.BytesIO()
            file.decrypt(output_file)
            output_file.seek(0)
            with pd.ExcelFile(output_file) as xls:
                factory_list = []
                # 循环每一个sheet
                for sheet_name in xls.sheet_names:
                    df = pd.read_excel(xls, sheet_name=sheet_name, header=0)
                    if '日期' not in df.columns:
                        continue
                    for index, row in df.iterrows():
                        # 如果内容为空或者为/就设置为空
                        row = row.replace({' ': None, '/': None})
                        row = row.where(pd.notnull(row), None)
                        # 如果日期这列没有数据就跳过该行内容
                        if row["日期"] is None:
                            continue
                        # 处理成日期格式（44591表格中的数据接收就变成这样了要转换成日期格式）
                        try:
                            date = (pd.to_datetime('1900-01-01') + pd.to_timedelta(row["日期"] - 2, 'D')).date()
                        except Exception as e:
                            date = pd.to_datetime(row[0], errors='coerce')
                            if pd.notnull(date):
                                date = date.strftime("%Y-%m-%d")
                            else:
                                continue
                        try:
                            num = row["件数"]
                        except KeyError:
                            try:
                                num = row["件数/米数"]
                            except KeyError:
                                num = None
                        # 把数据转换成模型类对象并存入列表中
                        factory = Factory(
                            code=row["款号"],
                            date=date,
                            price=row["总金额"],
                            num=num,
                            factory=sheet_name,
                            file_name=excel_file.name,
                        )
                        factory_list.append(factory)
                with transaction.atomic():
                    # 对本日的内容进行覆盖
                    Factory.objects.filter(file_name=excel_file.name).delete()
                    inserted_count = Factory.objects.bulk_create(factory_list)
                    return JsonResponse({'message': f'{len(inserted_count)} 条数据更新成功。'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class StyleStatusView(APIView):
    def get(self, request):
        """
        查询获取并返回新款状态数据
        :param request:
        :return:
        """
        # 款号
        code = request.query_params.get('code')
        # 标签
        tags = request.query_params.get('tags')
        # 是否导出
        is_all = request.query_params.get('is_all')
        # 是否去重
        dis = request.query_params.get('dis')
        # 上传日期
        date_time = request.query_params.getlist('date_time[]')
        queryset = StyleStatus.objects.all().order_by('-time')
        conditions = {}
        if code:
            conditions['code'] = code
        # 根据前端传的日期筛选出上传日期在这个范围内的内容
        if date_time:
            conditions['date_time__range'] = (date_time[0], date_time[1])
        if tags:
            tags_list = tags.split(',')
            tags_query = Q()
            for tag in tags_list:
                if tag == '其他':
                    tags_query &= Q(is_other=True)
                else:
                    tags_query &= Q(tags__contains=tag)
            queryset = queryset.filter(tags_query)
        if conditions:
            queryset = queryset.filter(**conditions).order_by('-time')
        if dis == 'true':
            subquery = queryset.filter(date_time=OuterRef('date_time'), code=OuterRef('code')).order_by(
                '-time')
            queryset = queryset.filter(time=Subquery(subquery.values('time')[:1]))
        if is_all == "1":
            serializer = StyleStatusSerializer(queryset, many=True)
            return Response(serializer.data)
        # 这里添加了分页
        paginator = OrderPagination()
        page = paginator.paginate_queryset(queryset, request)

        if page is not None:
            serializer = StyleStatusSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        serializer = StyleStatusSerializer(queryset, many=True)
        return Response(serializer.data)

    def patch(self, request):
        """
        修改对应id的信息
        :param request:
        :return:
        """

        id = request.data.get('id')
        # 标签
        tags = request.data.get('tags')
        # 备注
        remarks = request.data.get('remarks')
        conditions = {}
        if tags:
            tags_list = tags.split(',')
            # 定义的正常标签如果不在其中就是其他标签
            normal_tags = ['采购面料', '采购辅料', '没到车间', '刚到车间', '车间加工中', '在后道', '入仓', '到档口',
                           '新款', '翻单', '在档口']
            for tag in tags_list:
                # 如果添加的标签不是定义的标签就把改条数据标记为有其他标签
                if tag not in normal_tags:
                    conditions["is_other"] = True
                else:
                    conditions["is_other"] = False
            conditions['tags'] = tags
        if remarks:
            conditions['remarks'] = remarks
        try:
            if conditions:
                StyleStatus.objects.filter(pk=id).update(**conditions)
            return JsonResponse({'message': f'修改成功'}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def insert_style_status(status_time, date_time, tag, code):
    """
    根据款号生成该款号的每天状态并插入数据库
    :param status_time: 下单日期
    :param date_time: 报表上传日期
    :param tag: 标签
    :param code: 款号
    :return:
    """
    query = """
        INSERT INTO
        taiwei_style_status
        (time,date_time,code,cai_chuang,che_jian,hou_dao,
        tai_wei,yi_fa,mo_ya,fabric_price,materials_price,factory_price,
        salesrecord_price,order_price,to_salesrecord_time,time_num,tags,
        is_other,num)
        SELECT
            %s,
            %s,
            a.*,
            e.price AS fabric_price,
            d.price AS material_price,
            f.price AS factory_price,
            c.total as salesrecord_price,
            b.order_total_amount,	
            g.registration_time as to_salesrecord_time,
            %s as time_num,
            CONCAT_WS(',',
                IF(d.is_taiwei_materials IS NOT NULL, '采购面料', NULL),   #采购面料
                IF(e.is_taiwei_fabric IS NOT NULL, '采购辅料', NULL),			#采购辅料
                IF(
                    (DATE_SUB(CURDATE(), INTERVAL 20 DAY) <= %s)
                    AND
                    ((status = '新款' AND 
                    ((a.cai_chuang+a.che_jian+a.hou_dao+a.tai_wei+a.yi_fa+a.mo_ya) = 0))
                    OR
                    (status = '翻单' AND (t.inventory2>0 OR a.che_jian<=s.che_jian))),
                    '没到车间',
                    NULL
                ),						#没到车间
                IF((a.che_jian-s.che_jian)>=10, '刚到车间', NULL),						#刚到车间
                IF((a.che_jian = s.che_jian) AND a.che_jian>11, '车间加工中', NULL),			#车间加工中
                IF((a.hou_dao = s.hou_dao) AND a.hou_dao>11, '在后道', NULL),			#在后道
                IF(a.hou_dao < s.hou_dao, '入仓', NULL),						#入仓
                IF(g.is_taiwei_stock_in IS NOT NULL, '到档口', NULL),			#到档口
                IF(t.inventory !=0,'在档口',NULL),			#在档口
                %s
            ) as tags,
            0,
            b.num
        FROM (
            SELECT
                code,
                SUM(CASE WHEN house like "裁床%%" THEN inventory ELSE 0 END) AS cai_chuang,
                SUM(CASE WHEN house like "%%车间%%" THEN inventory ELSE 0 END) AS che_jian,
                SUM(CASE WHEN house like "%%后道%%" THEN inventory ELSE 0 END) AS hou_dao,
                SUM(CASE WHEN house like "%%泰维%%" THEN inventory ELSE 0 END) AS tai_wei,
                SUM(CASE WHEN house like "%%意法%%" THEN inventory ELSE 0 END) AS yi_fa,
                SUM(CASE WHEN house like "%%茉雅%%" THEN inventory ELSE 0 END) AS mo_ya
            FROM taiwei_stock
            WHERE code = %s
            GROUP BY code
        ) AS a
        LEFT JOIN (
            SELECT
                LEFT(merchant_code, LENGTH(merchant_code)-1) AS code,
                (
                SELECT 
                SUM(order_total_amount) AS order_total_amount
                FROM 
                taiwei_orders
                 WHERE order_status = '已完成' AND 
                 (after_sale_status LIKE '%%售后关闭%%' OR after_sale_status = '-') AND 
                 LEFT(merchant_code, LENGTH(merchant_code)-1) = %s
                 GROUP BY LEFT(merchant_code, LENGTH(merchant_code)-1)
                ) as order_total_amount,
                COUNT(DISTINCT DATE(order_submit_time)) as num
            FROM taiwei_orders
            WHERE LEFT(merchant_code, LENGTH(merchant_code)-1) = %s
            GROUP BY LEFT(merchant_code, LENGTH(merchant_code)-1)
        ) AS b ON  b.code = a.code
        LEFT JOIN (
            SELECT
                product_code AS code,
                SUM(total) AS total
            FROM taiwei_salesrecord
            WHERE product_code = %s
            GROUP BY product_code
        ) AS c ON  c.code = a.code
        LEFT JOIN (
            SELECT
                merchant_code,
                SUM(price) AS price,
                (
                    SELECT merchant_code FROM taiwei_materials WHERE DATE(`time`) = CURDATE() AND merchant_code = %s
                ) as is_taiwei_materials
            FROM taiwei_materials
            WHERE merchant_code = %s
            GROUP BY merchant_code
        ) AS d ON d.merchant_code = a.code
        LEFT JOIN (
            SELECT
                merchant_code,
                SUM(price) AS price,
                (
                    SELECT merchant_code FROM taiwei_fabric WHERE DATE(`time`) = CURDATE() AND merchant_code = %s
                ) as is_taiwei_fabric
            FROM taiwei_fabric
            WHERE merchant_code = %s
            GROUP BY merchant_code
        ) AS e ON  e.merchant_code = a.code
        LEFT JOIN (
            SELECT
                code,
                SUM(price) AS price
            FROM taiwei_factory
            WHERE code = %s
            GROUP BY code
        ) AS f ON f.code = a.code
        LEFT JOIN(
            SELECT
            *
            FROM 
            taiwei_style_status
            WHERE code = %s
            AND date_time != CURDATE()
            ORDER BY date_time desc
            LIMIT 1
        )as s ON  s.code = a.code
        
        LEFT JOIN
        (
        SELECT
        product_code,
        DATE(MAX(registration_time)) as registration_time,
        (
            SELECT product_code FROM taiwei_stock_in WHERE DATE(`registration_time`) = CURDATE() AND product_code = %s
        ) is_taiwei_stock_in
        FROM
        taiwei_stock_in
        WHERE product_code = %s
        GROUP BY product_code
        ) as g ON g.product_code = a.code
        LEFT JOIN
        (
            SELECT
            code,
            SUM(CASE WHEN house="意法仓" OR house="vege档口" OR house="MOIA档口" THEN inventory ELSE 0 END) as inventory,
            SUM(CASE WHEN house="积聚仓" OR house="裁床" THEN inventory ELSE 0  END ) as inventory2,
            %s as status
            FROM
            taiwei_stock
            WHERE code=%s
            GROUP BY code 
        ) as t on t.code = a.code
    """
    # 计算出下单到今日的天数
    difference = date_time - status_time
    difference_in_days = difference.days

    with connection.cursor() as cursor:
        cursor.execute(query,
                       [status_time, date_time, difference_in_days, status_time, tag, code, code, code, code,
                        code, code, code, code, code, code, code, code, tag, code])


def insert_new_style_status_tracking(order_date, total_quantity, status, code):
    """
    插入新款跟踪数据
    :param order_date: 下单日期
    :param total_quantity: 总件数
    :param status: 新款还是翻单
    :param code:   款号
    :return:
    """
    query = """	
        INSERT INTO taiwei_new_style_status_tracking
        (code,order_date,expected_date,total_quantity,status,
        label,caichuang_stock,chejian_stock,
        houdao_stock,taiwei_stock,yifa_stock,moya_stock)
        (
        SELECT
        code,
        %s AS order_date,
        DATE_ADD(%s, INTERVAL 10 DAY) AS expected_date,
        %s AS total_quantity,
        %s AS status,
        "1"	AS label,
        SUM(CASE WHEN house like "裁床%%" THEN inventory ELSE 0 END) AS caichuang_stock,
        SUM(CASE WHEN house like "%%车间%%" THEN inventory ELSE 0 END) AS chejian_stock,
        SUM(CASE WHEN house like "%%后道%%" THEN inventory ELSE 0 END) AS houdao_stock,
        SUM(CASE WHEN house like "%%泰维%%" THEN inventory ELSE 0 END) AS taiwei_stock,
        SUM(CASE WHEN house like "%%意法%%" THEN inventory ELSE 0 END) AS yifa_stock,
        SUM(CASE WHEN house like "%%茉雅%%" THEN inventory ELSE 0 END) AS moya_stock
        FROM taiwei_stock
        WHERE code = %s
        GROUP BY code
        )
    """

    with connection.cursor() as cursor:
        cursor.execute(query, [order_date, order_date, total_quantity, status, code])


class NewStyleStatusTrackingView(APIView):
    def get(self, request):
        queryset1 = NewStyleStatusTracking.objects.filter(label="1")
        queryset2 = NewStyleStatusTracking.objects.filter(label="2")
        queryset3 = NewStyleStatusTracking.objects.filter(label="3")
        queryset4 = NewStyleStatusTracking.objects.filter(label="4")
        queryset5 = NewStyleStatusTracking.objects.filter(label="5")
        queryset6 = NewStyleStatusTracking.objects.filter(label="6")
        serializers1 = NewStyleStatusTrackingSerializer(instance=queryset1, many=True)
        serializers2 = NewStyleStatusTrackingSerializer(instance=queryset2, many=True)
        serializers3 = NewStyleStatusTrackingSerializer(instance=queryset3, many=True)
        serializers4 = NewStyleStatusTrackingSerializer(instance=queryset4, many=True)
        serializers5 = NewStyleStatusTrackingSerializer(instance=queryset5, many=True)
        serializers6 = NewStyleStatusTrackingSerializer(instance=queryset6, many=True)

        data = {
            "data1": serializers1.data,
            "data2": serializers2.data,
            "data3": serializers3.data,
            "data4": serializers4.data,
            "data5": serializers5.data,
            "data6": serializers6.data,
        }
        return JsonResponse(data)

    def patch(self, request):
        id = request.data.get('id')
        label = request.data.get('label')
        expected_date = request.data.get('expected_date')
        conditions = {}
        if label:
            conditions["label"] = label
        if expected_date:
            conditions["expected_date"] = expected_date
        try:
            if conditions:
                NewStyleStatusTracking.objects.filter(pk=id).update(**conditions)
            return JsonResponse({'message': "success"}, status=200)
        except Exception as e:
            return JsonResponse({'err': str(e)}, status=500)


def move_new_style_status_tracking(request):
    try:
        with transaction.atomic():
            for i in range(4):
                with connection.cursor() as cursor:
                    cursor.callproc('move')  # Name of your stored procedure
        return JsonResponse({'message': 'Procedure executed successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'err': str(e)}, status=500)
