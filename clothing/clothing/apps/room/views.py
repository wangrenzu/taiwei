import asyncio
from django_redis import get_redis_connection
from rest_framework.views import APIView
from datetime import datetime, timedelta
from .models import Room, Integration
from .serializers import RoomSerializer, IntegrationSerializer
from rest_framework.response import Response

from clothing.util.getGood import getGoods, getGoodsSencode, getLive, fetch_barrage
from django.db import connection
from django.core.cache import cache


class RoomView(APIView):

    def get(self, request):
        date_time = request.query_params.get('date_time')
        if date_time:
            date_time = datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S.%fZ")
            previous_day = date_time + timedelta(days=1)
            date_time = previous_day.strftime("%Y-%m-%d")
        else:
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            date_time = date_str

        room_name = request.query_params.get('room_name') or 'S姐直播间'
        session = request.query_params.get('session') or '第一场'

        query = '''
            SELECT
                MAX(a.id) as id,
				MAX(a.product_id) as product_id,
				MAX(a.code) as code,
				MAX(a.img) as img,
				MAX(a.characteristic) as characteristic,
				MAX(b.back_num) as back_num,
				MAX(b.pending_and_in_transit_num) as pending_and_in_transit_num,
				MAX(a.exposure) as exposure,
				MAX(a.clickExposure) as clickExposure,
				MAX(a.clickDeal) as clickDeal,
				MAX(a.salesPrice) as salesPrice,
				MAX(a.salesNum) as salesNum,
				MAX(a.order_number) as order_number,
				MAX(a.order_rate) as order_rate,
				MAX(a.back_rate) as back_rate,
				MAX(a.clickDeal2) as clickDeal2,
				MAX(a.GPM) as GPM,
				MAX(c.exposure) as cart_exposure,
				MAX(c.clickExposure) as cart_clickExposure,
				MAX(c.clickDeal) as cart_clickDeal,
				MAX(c.salesPrice) as cart_salesPrice,
				MAX(c.salesNum) as cart_salesNum,
				MAX(c.order_number) as prev_order_number,
				MAX(c.order_rate) as prev_order_rate,
				MAX(c.back_rate) as prev_back_rate,
				MAX(c.clickDeal2) as prev_clickDeal2,
				MAX(c.GPM) as prev_GPM
				FROM
				(
				SELECT 
				id,
				product_id,
				code,
				img,
				characteristic,
				exposure,
				clickExposure,
				clickDeal,
				salesPrice,
				salesNum,
				order_number,
				order_rate,
				back_rate,
				clickDeal2,
				GPM
				FROM taiwei_room
				WHERE room_name = %s
				AND date_time = %s
				AND session = %s
				)as a
				
				LEFT JOIN
				(
					SELECT
					id,
					product_id,
					code,
					img,
					characteristic,
					exposure,
					clickExposure,
					clickDeal,
					salesPrice,
					salesNum,
					date_time,
					session,
					room_name,
					order_number,
					order_rate,
					back_rate,
					clickDeal2,
					GPM
			FROM
					taiwei_room
			WHERE
			date_time != %s
				AND date_time = (
						SELECT
								MAX(date_time)
						FROM
								taiwei_room AS t2
						WHERE
						t2.code = taiwei_room.code
						AND t2.date_time != %s
						AND room_name = %s
						)
				)as c
				ON a.code = c.code
						
				LEFT JOIN
				
				(
					SELECT
						code,
						MAX(sum_total_amount_3) as back_price,
						MAX(sum_product_quantity_3) as back_num,
						MAX(pending_and_in_transit) as pending_and_in_transit,
						MAX(pending_and_in_transit_num) as pending_and_in_transit_num
					FROM
					(
						SELECT 
							LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) AS code, 
							SUM(o.order_total_amount) AS sum_total_amount_3, 
							SUM(o.product_quantity) AS sum_product_quantity_3,
							0 AS pending_and_in_transit,
							0 AS pending_and_in_transit_num
						FROM taiwei_orders AS o
						WHERE o.order_status = '已关闭'
							AND o.after_sale_status LIKE '%%退款成功%%'
							AND (o.merchant_remark NOT LIKE '%%退货%%' AND o.merchant_remark NOT LIKE '%%拒收%%' AND o.merchant_remark NOT LIKE '%%退回%%')
							AND DATE(o.order_submit_time) = CURDATE()
							AND o.ad_channel != '直播'
							AND o.influencer_nickname LIKE %s
						GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)

						UNION ALL

						SELECT 
							LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1) AS code, 
							0 AS sum_total_amount_3, 
							0 AS sum_product_quantity_3,
							SUM(order_total_amount) as pending_and_in_transit,
							SUM(product_quantity) AS pending_and_in_transit_num
						FROM taiwei_orders AS o
						WHERE ((o.order_status = '已发货' AND (o.after_sale_status LIKE '%%售后关闭%%' OR o.after_sale_status = '-')) 
						OR (o.order_status = '待发货' AND o.after_sale_status = '-'))
							AND DATE(o.order_submit_time) = CURDATE()
							AND o.ad_channel != '直播'
							AND o.influencer_nickname LIKE %s
						GROUP BY LEFT(o.merchant_code, LENGTH(o.merchant_code) - 1)
					) as a
					GROUP BY code
				) as b
				ON a.code LIKE CONCAT('%%', b.code, '%%')
				GROUP BY a.code	
        '''
        queryset = Room.objects.raw(query, [room_name, date_time, session, date_time, date_time,
                                            room_name, f'%{room_name[:2]}%', f'%{room_name[:2]}%'])
        serializer = RoomSerializer(queryset, many=True)
        try:
            room_live_code = request.query_params.get('room_live_code')
            code = cache.get('code')[0]
            if room_live_code:
                live_code = room_live_code
            else:
                live_code = code[0]
            # code = ['04112', '58',
            #         'https://p9-aio.ecombdimg.com/obj/ecom-shop-material/PheaHqHs_m_85287e3d0da2afa47527761e03ade962_sx_491791_www1030-1030']
            query2 = """
                SELECT
                taiwei_integration.*,
                %s as img,
                %s as product_id,
                %s as r_code
                FROM
                taiwei_integration
                WHERE code LIKE %s
                ORDER BY creation_date DESC LIMIT 1
            """
            queryset2 = Integration.objects.raw(query2, [code[2], code[1], live_code, '%' + str(live_code)])
            serializer2 = IntegrationSerializer(queryset2, many=True)
            data2 = serializer2.data
            data4 = code[0]
        except Exception as e:
            data2 = None
            data4 = None
        try:
            data3 = cache.get('data3')
        except Exception as e:
            data3 = None
        return Response({'data1': serializer.data, 'data2': data2, 'data3': data3, 'data4': data4})

    def patch(self, request):
        id = request.data.get('id')
        code = request.data.get('code')
        Room.objects.filter(id=id).update(code=code)
        return Response({'status': 'success'}, status=200)

    def post(self, request):
        room_name = request.data.get('room_name')
        room_id = request.data.get('room_id')
        success = False
        getUrl = False
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")

        while not success:
            try:
                if room_name == 'S姐直播间':
                    rooms = Room.objects.filter(date_time=date_str, room_name='S姐直播间')
                    if not rooms.exists():
                        getUrl = True
                    data1 = getGoods("127.0.0.1:9531", room_id, getUrl)
                    data2 = getGoodsSencode("127.0.0.1:9531", room_id)
                    data3 = getLive("127.0.0.1:9531", room_id)
                    cache.set('data3', data3)
                elif room_name == '悦仓直播间':
                    rooms = Room.objects.filter(date_time=date_str, room_name='悦仓直播间')
                    if not rooms.exists():
                        getUrl = True
                    data1 = getGoods("127.0.0.1:9532", room_id, getUrl)
                    data2 = getGoodsSencode("127.0.0.1:9532", room_id)
                    data3 = getLive("127.0.0.1:9532", room_id)
                    cache.set('data3', data3)
                elif room_name == '星露直播间':
                    rooms = Room.objects.filter(date_time=date_str, room_name='星露直播间')
                    if not rooms.exists():
                        getUrl = True
                    data1 = getGoods("127.0.0.1:9533", room_id, getUrl)
                    data2 = getGoodsSencode("127.0.0.1:9533", room_id)
                    data3 = getLive("127.0.0.1:9533", room_id)
                    cache.set('data3', data3)
                success = True
            except Exception as e:
                print(e)
                return Response({'status': 'error', 'message': str(e)}, status=500)
        try:
            Room.objects.filter(date_time=date_str, room_name=room_name).delete()
        except Exception as e:
            print(e)
        for item in data1:
            if item[2] == data2[0][0]:
                self.code = []
                self.code.append([data2[0][0], item[0], item[1]])
                cache.set('code', self.code)
                break

        data2_dict = {row[0]: row[1:] for row in data2}

        empty_row = [None] * len(data2[0][1:])

        merged_data = [row + data2_dict.get(row[2], empty_row) for row in data1]
        # 检查并填充缺失的数据
        for result in merged_data:
            query = '''
                SELECT id,merchant_code FROM taiwei_goods WHERE merchant_code LIKE %s ORDER BY id LIMIT 1
            '''
            with connection.cursor() as cursor:
                cursor.execute(query, [f'%{result[2]}'])
                row = cursor.fetchone()  # 获取查询结果的第一行
                if row:
                    id, merchant_code = row
                else:
                    merchant_code = result[2]

            room = Room()
            room.product_id = int(result[0])
            room.img = result[1]
            room.code = merchant_code
            room.characteristic = result[3]
            room.exposure = int(result[4])
            room.clickExposure = result[5]
            room.clickDeal = result[6]
            room.salesPrice = result[7]
            room.salesNum = int(result[8])
            room.room_name = room_name
            room.order_number = int(result[9]) if result[9] is not None else None
            room.order_rate = result[10]
            room.back_rate = result[11]
            room.clickDeal2 = result[12]
            room.GPM = result[13]
            room.save()
        return Response({'status': 'success'}, status=200)


class IntegrationView(APIView):
    def patch(self, request):
        code = request.data.get('code')
        price = request.data.get('price')
        try:
            Integration.objects.filter(code=code).update(order_price=price)
            return Response({'status': 'success'}, status=200)
        except Exception as e:
            return Response({'status': 'error'}, status=500)


class Barrage(APIView):
    def get(self, request):
        try:
            room_name = request.query_params.get("room_name")
            room_id = request.query_params.get("room_id")
            conn = get_redis_connection("default")
            val = int(conn.get(room_name).decode())
            if val == 1:
                if room_name == "S姐直播间":
                    fetch_barrage.delay("127.0.0.1:9531", room_id, room_name)
                if room_name == "悦仓直播间":
                    fetch_barrage.delay("127.0.0.1:9532", room_id, room_name)
                if room_name == "星露直播间":
                    fetch_barrage.delay("127.0.0.1:9533", room_id, room_name)
            return Response({'status': 'success'}, status=200)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=500)
