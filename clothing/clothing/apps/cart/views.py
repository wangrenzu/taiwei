import json

import pandas as pd
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db import connection

from .models import Product
from .serializers import ProductSerializer


# Create your views here.


class CartInfo(APIView):
    # 添加商品到购物车
    def post(self, request):
        # 款号
        code = request.data.get('code')
        # 购物车名称
        cart_name = request.data.get('cart_name')
        # 来源
        source = request.data.get('source')
        query = '''
                INSERT INTO 
                taiwei_product
                (commodity_code,product_name,image,order_quantity,workshop_quantity,
                workshop_quantity_num,post_processing_quantity,post_processing_quantity_num,
                taiwei_yifa_moyajia_quantity,taiwei_yifa_moyajia_quantity_num,pending_and_in_transit,
                cancelled,successful,returned,price,live_deal_conversion_rate,exposure_click_rate,
                max_exposure_quantity,avg_live_exposure_count,prediction,prediction_money,cart_name,
                source,exposure,clickExposure,clickDeal)
                SELECT 
                a.code as commodity_code,
                d.category as product_name,
                b.commodity_image as image,
                a.order_quantity  as order_quantity ,
                a.workshop_quantity as workshop_quantity,
                a.workshop_quantity_num as workshop_quantity_num,
                a.post_processing_quantity as post_processing_quantity,
                a.post_processing_quantity_num as post_processing_quantity_num,
                a.taiwei_yifa_moyajia_quantity as taiwei_yifa_moyajia_quantity,
                a.taiwei_yifa_moyajia_quantity_num as taiwei_yifa_moyajia_quantity_num,
                b.pending_shipment as pending_and_in_transit,
                b.cancelled as cancelled,
                b.successful as successful,
                b.returned as returned,
                c.price as price,
                b.live_deal_conversion_rate as live_deal_conversion_rate,
                b.exposure_click_rate as exposure_click_rate,
                b.max_live_exposure_count as max_exposure_quantity,
                b.avg_live_exposure_count as avg_live_exposure_count,
                b.avg_live_exposure_count * b.live_deal_conversion_rate * b.exposure_click_rate as prediction,
                (b.avg_live_exposure_count * b.live_deal_conversion_rate * b.exposure_click_rate) * c.price as prediction_money,
                %s,
                %s,
                e.exposure,
                e.clickExposure,
                e.clickDeal
                FROM		
                (SELECT 
                    n.code,
                    n.workshop_quantity_num as workshop_quantity_num,
                    n.post_processing_quantity_num as post_processing_quantity_num,
                    n.taiwei_yifa_moyajia_quantity_num as taiwei_yifa_moyajia_quantity_num,    
                    SUM(n.order_quantity) as order_quantity,
                    (
                        SELECT GROUP_CONCAT(workshop SEPARATOR '  ')
                        FROM (
                            SELECT CONCAT(cls, '-', SUM(CASE WHEN house LIKE '%%车间%%' THEN inventory ELSE 0 END)) AS workshop
                            FROM taiwei_newstock
                            WHERE code = %s
                            GROUP BY code, cls
                        ) AS subquery
                    ) AS workshop_quantity,
                    (
                        SELECT GROUP_CONCAT(post_processing SEPARATOR '  ')
                        FROM (
                            SELECT CONCAT(cls, '-', SUM(CASE WHEN house LIKE '%%后道%%' THEN inventory ELSE 0 END)) AS post_processing
                            FROM taiwei_newstock
                            WHERE code = %s
                            GROUP BY code, cls
                        ) AS subquery
                    ) AS post_processing_quantity ,
                    (
                        SELECT GROUP_CONCAT(taiwei_yifa_moyajia SEPARATOR '  ')
                        FROM (
                            SELECT CONCAT(cls, '-', SUM(CASE WHEN (house LIKE '%%泰维%%' OR house LIKE '%%意法%%' OR house LIKE '%%茉雅%%') THEN inventory ELSE 0 END)) AS taiwei_yifa_moyajia
                            FROM taiwei_newstock
                            WHERE code = %s
                            GROUP BY code, cls
                        ) AS subquery
                    ) AS taiwei_yifa_moyajia_quantity 
                FROM (
                    SELECT
                        code,
                        SUM(CASE WHEN house LIKE '%%车间%%' THEN inventory ELSE 0 END) as workshop_quantity_num,
                        SUM(CASE WHEN house LIKE '%%后道%%' THEN inventory ELSE 0 END)as post_processing_quantity_num,
                        SUM(CASE WHEN (house LIKE '%%泰维%%' OR house LIKE '%%意法%%' OR house LIKE '%%茉雅%%') THEN inventory ELSE 0 END) as taiwei_yifa_moyajia_quantity_num,
                        SUM(order_quantity) as order_quantity
                    FROM
                        taiwei_newstock
                    WHERE
                        code = %s
                    GROUP BY
                        code
                ) AS n
                GROUP BY n.code
                ) as a

                LEFT JOIN
                (SELECT 
                    o.code,
                    o.category,
                    c.commodity_image,
                    o.pending_shipment,
                    o.cancelled,
                    o.successful,
                    o.returned,
                    c.live_deal_conversion_rate,
                    c.exposure_click_rate,
                    c.max_live_exposure_count,
                    c.avg_live_exposure_count
                    
                FROM (
                    SELECT
                        o.code,
                        MAX(o.cancelled) as cancelled,
                        MAX(o.pending_shipment) as pending_shipment,
                        MAX(o.successful) as successful,
                        MAX(o.returned) as returned,
                        MAX(o.category) as category,
                        MAX(o.product_id) as product_id
                    FROM (
                        SELECT 
                            LEFT(merchant_code, LENGTH(merchant_code) - 1) AS code,
                            SUM(product_quantity) AS cancelled,
                            0 AS pending_shipment,
                            0 AS successful,
                            0 AS returned,
                            MAX(product_id) as product_id,
                            REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
                        FROM taiwei_orders 
                        WHERE (order_status = '已关闭' AND 
                            (after_sale_status LIKE '%%退款成功%%' AND 
                            (merchant_remark LIKE '%%取消%%' OR merchant_remark='nan'))) 
                            AND LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s
                            AND order_submit_time >= CURDATE() - INTERVAL 15 DAY
                        GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)

                        UNION ALL

                        SELECT 
                            LEFT(merchant_code, LENGTH(merchant_code) - 1) AS code,
                            0 AS cancelled,
                            SUM(product_quantity) AS pending_shipment,
                            0 AS successful,
                            0 AS returned,
                            MAX(product_id) as product_id,
                            REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
                        FROM taiwei_orders  
                        WHERE ((order_status = '已发货' AND 
                            (after_sale_status LIKE '%%售后关闭%%' OR after_sale_status = '-')) 
                            OR (order_status = '待发货' AND after_sale_status = '-'))
                            AND LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s 
                            AND order_submit_time >= CURDATE() - INTERVAL 15 DAY
                        GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)

                        UNION ALL

                        SELECT 
                            LEFT(merchant_code, LENGTH(merchant_code) - 1) AS code,
                            0 AS cancelled,
                            0 AS pending_shipment,
                            SUM(product_quantity) AS successful,
                            0 AS returned,
                            MAX(product_id) as product_id,
                            REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
                        FROM taiwei_orders  
                        WHERE (order_status = '已完成' AND 
                            (after_sale_status LIKE '%%售后关闭%%' OR after_sale_status = '-'))  
                            AND LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s
                            AND order_submit_time >= CURDATE() - INTERVAL 15 DAY
                        GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)

                        UNION ALL

                        SELECT
                            LEFT(merchant_code, LENGTH(merchant_code) - 1) AS code,
                            0 AS cancelled,
                            0 AS pending_shipment,
                            0 AS successful,
                            SUM(product_quantity) AS returned,
                            MAX(product_id) as product_id,
                            REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
                        FROM taiwei_orders  
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
                            AND order_submit_time >= CURDATE() - INTERVAL 15 DAY
                        GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)
                    ) AS o
                    GROUP BY o.code
                ) AS o
                LEFT JOIN (
                    SELECT
                            code,
                            MAX(commodity_image) as commodity_image,
                            MAX(live_deal_conversion_rate) as live_deal_conversion_rate,
                            MAX(exposure_click_rate) as exposure_click_rate,
                            MAX(avg_live_exposure_count) as avg_live_exposure_count,
                            MAX(max_live_exposure_count) as max_live_exposure_count
                            FROM
                            (
                            SELECT  
                            %s as code,
                            c.commodity_code,
                            c.commodity_image,
                            c.live_deal_conversion_rate,
                            c.live_click_count / 
                            (
                            CASE WHEN c.live_exposure_count=0 THEN 1 ELSE c.live_exposure_count END
                            ) as exposure_click_rate,
                            (
                            SELECT 
                            AVG(CASE WHEN oc.live_exposure_count > 1000 THEN oc.live_exposure_count ELSE NULL END) as avg_live_exposure_count
                            FROM taiwei_onecommodity AS oc
                            WHERE oc.date_time >= CURDATE() - INTERVAL 3 DAY
                                AND oc.commodity_code = c.commodity_code
                            ) AS avg_live_exposure_count,
                            (
                            SELECT MAX(oc.live_exposure_count)
                            FROM taiwei_onecommodity AS oc
                            WHERE oc.date_time >= CURDATE() - INTERVAL 3 DAY
                                AND oc.commodity_code = c.commodity_code
                            ) AS max_live_exposure_count
                            FROM taiwei_commodity AS c
                        WHERE c.commodity_code IN (SELECT product_id FROM taiwei_orders WHERE LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s)
                        ) as comm
                        GROUP BY code
                ) AS c ON o.code = c.code
                ) as b ON a.code = b.code
                LEFT JOIN(
                SELECT code, order_total_amount as price
                FROM (
                        SELECT LEFT(merchant_code, LENGTH(merchant_code) - 1) AS code, order_total_amount,
                                ROW_NUMBER() OVER (PARTITION BY LEFT(merchant_code, LENGTH(merchant_code) - 1) ORDER BY COUNT(*) DESC) AS rn
                        FROM taiwei_orders
                        WHERE LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s
                        GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1), order_total_amount
                ) subquery
                WHERE rn = 1
            ) as c ON b.code = c.code

            LEFT JOIN
            (
            SELECT
            merchant_code,
            category
            FROM taiwei_goods
            ) as d
            ON a.code = d.merchant_code
            LEFT JOIN
            (
                SELECT
                code,
                exposure,
                clickExposure,
                clickDeal,
                date_time
                FROM
                taiwei_room
                WHERE code = %s
                ORDER BY date_time DESC
                LIMIT 1
            )as e
            ON a.code = e.code
                        
                                        '''
        with connection.cursor() as cursor:
            cursor.execute(query,
                           [cart_name, source, code, code, code, code, code, code, code, code, code, code, code, code])
        return HttpResponse("OK")

    # 获取购物车信息
    def get(self, request):
        cart_name = request.query_params.getlist('cart_name')[0]
        queryset = Product.objects.filter(cart_name=cart_name)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    # 从购物车中删除某个商品
    def delete(self, request):
        id = request.query_params.get('id')
        Product.objects.get(pk=id).delete()
        return HttpResponse("ok")

    # 修改购物车状态信息
    def patch(self, request):
        code_list = request.data.get('code_list')

        query = '''
            INSERT INTO 
            taiwei_product
            (commodity_code,product_name,image,order_quantity,workshop_quantity,
            workshop_quantity_num,post_processing_quantity,post_processing_quantity_num,
            taiwei_yifa_moyajia_quantity,taiwei_yifa_moyajia_quantity_num,pending_and_in_transit,
            cancelled,successful,returned,price,live_deal_conversion_rate,exposure_click_rate,
            max_exposure_quantity,avg_live_exposure_count,prediction,prediction_money,cart_name,
            source,exposure,clickExposure,clickDeal)
            SELECT 
            a.code as commodity_code,
            d.category as product_name,
            b.commodity_image as image,
            a.order_quantity  as order_quantity ,
            a.workshop_quantity as workshop_quantity,
            a.workshop_quantity_num as workshop_quantity_num,
            a.post_processing_quantity as post_processing_quantity,
            a.post_processing_quantity_num as post_processing_quantity_num,
            a.taiwei_yifa_moyajia_quantity as taiwei_yifa_moyajia_quantity,
            a.taiwei_yifa_moyajia_quantity_num as taiwei_yifa_moyajia_quantity_num,
            b.pending_shipment as pending_and_in_transit,
            b.cancelled as cancelled,
            b.successful as successful,
            b.returned as returned,
            c.price as price,
            b.live_deal_conversion_rate as live_deal_conversion_rate,
            b.exposure_click_rate as exposure_click_rate,
            b.max_live_exposure_count as max_exposure_quantity,
            b.avg_live_exposure_count as avg_live_exposure_count,
            b.avg_live_exposure_count * b.live_deal_conversion_rate * b.exposure_click_rate as prediction,
            (b.avg_live_exposure_count * b.live_deal_conversion_rate * b.exposure_click_rate) * c.price as prediction_money,
            %s,
            %s,
            e.exposure,
            e.clickExposure,
            e.clickDeal
            FROM		
            (SELECT 
                n.code,
                n.workshop_quantity_num as workshop_quantity_num,
                n.post_processing_quantity_num as post_processing_quantity_num,
                n.taiwei_yifa_moyajia_quantity_num as taiwei_yifa_moyajia_quantity_num,    
                SUM(n.order_quantity) as order_quantity,
                (
                    SELECT GROUP_CONCAT(workshop SEPARATOR '  ')
                    FROM (
                        SELECT CONCAT(cls, '-', SUM(CASE WHEN house LIKE '%%车间%%' THEN inventory ELSE 0 END)) AS workshop
                        FROM taiwei_newstock
                        WHERE code = %s
                        GROUP BY code, cls
                    ) AS subquery
                ) AS workshop_quantity,
                (
                    SELECT GROUP_CONCAT(post_processing SEPARATOR '  ')
                    FROM (
                        SELECT CONCAT(cls, '-', SUM(CASE WHEN house LIKE '%%后道%%' THEN inventory ELSE 0 END)) AS post_processing
                        FROM taiwei_newstock
                        WHERE code = %s
                        GROUP BY code, cls
                    ) AS subquery
                ) AS post_processing_quantity ,
                (
                    SELECT GROUP_CONCAT(taiwei_yifa_moyajia SEPARATOR '  ')
                    FROM (
                        SELECT CONCAT(cls, '-', SUM(CASE WHEN (house LIKE '%%泰维%%' OR house LIKE '%%意法%%' OR house LIKE '%%茉雅%%') THEN inventory ELSE 0 END)) AS taiwei_yifa_moyajia
                        FROM taiwei_newstock
                        WHERE code = %s
                        GROUP BY code, cls
                    ) AS subquery
                ) AS taiwei_yifa_moyajia_quantity 
            FROM (
                SELECT
                    code,
                    SUM(CASE WHEN house LIKE '%%车间%%' THEN inventory ELSE 0 END) as workshop_quantity_num,
                    SUM(CASE WHEN house LIKE '%%后道%%' THEN inventory ELSE 0 END)as post_processing_quantity_num,
                    SUM(CASE WHEN (house LIKE '%%泰维%%' OR house LIKE '%%意法%%' OR house LIKE '%%茉雅%%') THEN inventory ELSE 0 END) as taiwei_yifa_moyajia_quantity_num,
                    SUM(order_quantity) as order_quantity
                FROM
                    taiwei_newstock
                WHERE
                    code = %s
                GROUP BY
                    code
            ) AS n
            GROUP BY n.code
            ) as a

            LEFT JOIN
            (SELECT 
                o.code,
                o.category,
                c.commodity_image,
                o.pending_shipment,
                o.cancelled,
                o.successful,
                o.returned,
                c.live_deal_conversion_rate,
                c.exposure_click_rate,
                c.max_live_exposure_count,
                c.avg_live_exposure_count

            FROM (
                SELECT
                    o.code,
                    MAX(o.cancelled) as cancelled,
                    MAX(o.pending_shipment) as pending_shipment,
                    MAX(o.successful) as successful,
                    MAX(o.returned) as returned,
                    MAX(o.category) as category,
                    MAX(o.product_id) as product_id
                FROM (
                    SELECT 
                        LEFT(merchant_code, LENGTH(merchant_code) - 1) AS code,
                        SUM(product_quantity) AS cancelled,
                        0 AS pending_shipment,
                        0 AS successful,
                        0 AS returned,
                        MAX(product_id) as product_id,
                        REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
                    FROM taiwei_orders 
                    WHERE (order_status = '已关闭' AND 
                        (after_sale_status LIKE '%%退款成功%%' AND 
                        (merchant_remark LIKE '%%取消%%' OR merchant_remark='nan'))) 
                        AND LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s
                        AND order_submit_time >= CURDATE() - INTERVAL 15 DAY
                    GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)

                    UNION ALL

                    SELECT 
                        LEFT(merchant_code, LENGTH(merchant_code) - 1) AS code,
                        0 AS cancelled,
                        SUM(product_quantity) AS pending_shipment,
                        0 AS successful,
                        0 AS returned,
                        MAX(product_id) as product_id,
                        REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
                    FROM taiwei_orders  
                    WHERE ((order_status = '已发货' AND 
                        (after_sale_status LIKE '%%售后关闭%%' OR after_sale_status = '-')) 
                        OR (order_status = '待发货' AND after_sale_status = '-'))
                        AND LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s 
                        AND order_submit_time >= CURDATE() - INTERVAL 15 DAY
                    GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)

                    UNION ALL

                    SELECT 
                        LEFT(merchant_code, LENGTH(merchant_code) - 1) AS code,
                        0 AS cancelled,
                        0 AS pending_shipment,
                        SUM(product_quantity) AS successful,
                        0 AS returned,
                        MAX(product_id) as product_id,
                        REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
                    FROM taiwei_orders  
                    WHERE (order_status = '已完成' AND 
                        (after_sale_status LIKE '%%售后关闭%%' OR after_sale_status = '-'))  
                        AND LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s
                        AND order_submit_time >= CURDATE() - INTERVAL 15 DAY
                    GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)

                    UNION ALL

                    SELECT
                        LEFT(merchant_code, LENGTH(merchant_code) - 1) AS code,
                        0 AS cancelled,
                        0 AS pending_shipment,
                        0 AS successful,
                        SUM(product_quantity) AS returned,
                        MAX(product_id) as product_id,
                        REGEXP_REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(MAX(product_name), '】', -1), '-', 1), '[a-zA-Z0-9]', '') AS category
                    FROM taiwei_orders  
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
                        AND order_submit_time >= CURDATE() - INTERVAL 15 DAY
                    GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1)
                ) AS o
                GROUP BY o.code
            ) AS o
            LEFT JOIN (
                SELECT
                        code,
                        MAX(commodity_image) as commodity_image,
                        MAX(live_deal_conversion_rate) as live_deal_conversion_rate,
                        MAX(exposure_click_rate) as exposure_click_rate,
                        MAX(avg_live_exposure_count) as avg_live_exposure_count,
                        MAX(max_live_exposure_count) as max_live_exposure_count
                        FROM
                        (
                        SELECT  
                        %s as code,
                        c.commodity_code,
                        c.commodity_image,
                        c.live_deal_conversion_rate,
                        c.live_click_count / c.live_exposure_count as exposure_click_rate,
                        (
                        SELECT 
                        AVG(CASE WHEN oc.live_exposure_count > 1000 THEN oc.live_exposure_count ELSE NULL END) as avg_live_exposure_count
                        FROM taiwei_onecommodity AS oc
                        WHERE oc.date_time >= CURDATE() - INTERVAL 3 DAY
                            AND oc.commodity_code = c.commodity_code
                                                        ) AS avg_live_exposure_count,
                                                        (
                        SELECT MAX(oc.live_exposure_count)
                        FROM taiwei_onecommodity AS oc
                        WHERE oc.date_time >= CURDATE() - INTERVAL 3 DAY
                            AND oc.commodity_code = c.commodity_code
                                                    ) AS max_live_exposure_count
                FROM taiwei_commodity AS c
                    WHERE c.commodity_code IN (SELECT product_id FROM taiwei_orders WHERE LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s)
                                                ) as comm
                                                GROUP BY code
            ) AS c ON o.code = c.code
            ) as b ON a.code = b.code
            LEFT JOIN(
            SELECT code, order_total_amount as price
            FROM (
                    SELECT LEFT(merchant_code, LENGTH(merchant_code) - 1) AS code, order_total_amount,
                            ROW_NUMBER() OVER (PARTITION BY LEFT(merchant_code, LENGTH(merchant_code) - 1) ORDER BY COUNT(*) DESC) AS rn
                    FROM taiwei_orders
                    WHERE LEFT(merchant_code, LENGTH(merchant_code) - 1) = %s
                    GROUP BY LEFT(merchant_code, LENGTH(merchant_code) - 1), order_total_amount
            ) subquery
            WHERE rn = 1
        ) as c ON b.code = c.code

        LEFT JOIN
        (
        SELECT
        merchant_code,
        category
        FROM taiwei_goods
        ) as d
        ON a.code = d.merchant_code
        LEFT JOIN
        (
            SELECT
            code,
            exposure,
            clickExposure,
            clickDeal,
            date_time
            FROM
            taiwei_room
            WHERE code = %s
            ORDER BY date_time DESC
            LIMIT 1
        )as e
        ON a.code = e.code
        '''

        Product.objects.filter(commodity_code__in=code_list).delete()
        with connection.cursor() as cursor:
            for code, cart_name in code_list.items():
                value = cart_name.split('/')
                cart_name = value[0]
                source = value[1]
                cursor.execute(query,
                               [cart_name, source, code, code, code, code, code, code, code, code, code, code, code,
                                code])
        return HttpResponse("ok")


def get_cart_link(request):
    # 获取购物车商品链接
    query = '''
        SELECT 
        LEFT(o.merchant_code, LENGTH(o.merchant_code)-1) as code,
        CONCAT('https://haohuo.jinritemai.com/ecommerce/trade/detail/index.html?id=',o.product_id)
        FROM taiwei_orders as o
        JOIN taiwei_commodity as c
        ON o.product_id = c.commodity_code
        WHERE LEFT(o.merchant_code, LENGTH(o.merchant_code)-1) = %s
        ORDER BY negative_review_rate,positive_review_count DESC,quality_return_rate
        LIMIT 1 
    '''
    codes = request.GET.getlist('codes')[0].split(',')  # 获取GET请求的查询参数
    try:
        with connection.cursor() as cursor:
            links = []
            for code in codes:
                cursor.execute(query, [code])
                result = cursor.fetchone()

                if result is not None:
                    link = {"code": result[0], "link": result[1]}
                    links.append(link)

            links_json = json.dumps(links)  # 将列表转换为JSON字符串
            return HttpResponse(links_json, content_type='application/json')
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


class find_code_link(APIView):
    def post(self, request):
        query = '''
                SELECT 
                LEFT(o.merchant_code, LENGTH(o.merchant_code)-1) as code,
                CONCAT('https://haohuo.jinritemai.com/ecommerce/trade/detail/index.html?id=',o.product_id)
                FROM taiwei_orders as o
                JOIN taiwei_commodity as c
                ON o.product_id = c.commodity_code
                WHERE LEFT(o.merchant_code, LENGTH(o.merchant_code)-1) = %s
                ORDER BY negative_review_rate,positive_review_count DESC,quality_return_rate
                LIMIT 1 
            '''
        excel_file = request.FILES.get('excel-file')

        df = pd.read_excel(excel_file, header=0)
        try:
            with connection.cursor() as cursor:
                links = []
                for index, row in df.iterrows():
                    code = row[1]
                    cursor.execute(query, [code])
                    result = cursor.fetchone()
                    if result is not None:
                        link = {"code": result[0], "link": result[1]}
                        links.append(link)
                links_json = json.dumps(links)  # 将列表转换为JSON字符串
                print(links_json)
                return HttpResponse(links_json, content_type='application/json')
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
