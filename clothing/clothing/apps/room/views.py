import asyncio
import traceback

from django.http import JsonResponse, HttpResponse
from django_redis import get_redis_connection
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from datetime import datetime, timedelta
from .models import Room, Integration, ProductInformation, LiveRoomData
from .serializers import RoomSerializer, IntegrationSerializer, ProductInfoSerializer, LiveRoomDataSerializer
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
            code = cache.get(f'{room_name}code')[0]
            if room_live_code:
                live_code = room_live_code
            else:
                live_code = code[0]
            # code = ['04112', '58',
            #         'https://p9-aio.ecombdimg.com/obj/ecom-shop-material/PheaHqHs_m_85287e3d0da2afa47527761e03ade962_sx_491791_www1030-1030']
            # live_code = "04112"
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
            data3 = cache.get(room_name)
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
                    cache.set(room_name, data3)
                elif room_name == '悦仓直播间':
                    rooms = Room.objects.filter(date_time=date_str, room_name='悦仓直播间')
                    if not rooms.exists():
                        getUrl = True
                    data1 = getGoods("127.0.0.1:9532", room_id, getUrl)
                    data2 = getGoodsSencode("127.0.0.1:9532", room_id)
                    data3 = getLive("127.0.0.1:9532", room_id)
                    cache.set(room_name, data3)
                elif room_name == '星露直播间':
                    rooms = Room.objects.filter(date_time=date_str, room_name='星露直播间')
                    if not rooms.exists():
                        getUrl = True
                    data1 = getGoods("127.0.0.1:9533", room_id, getUrl)
                    data2 = getGoodsSencode("127.0.0.1:9533", room_id)
                    data3 = getLive("127.0.0.1:9533", room_id)

                    cache.set(room_name, data3)
                success = True
            except Exception as e:
                print(e)
                return Response({'status': 'error', 'message': str(e)}, status=500)
        try:
            Room.objects.filter(date_time=date_str, room_name=room_name).delete()
        except Exception as e:
            print(e)
            return Response({'status': 'error', 'message': str(e)}, status=500)
        for item in data1:
            if item[2] == data2[0][0]:
                self.code = []
                self.code.append([data2[0][0], item[0], item[1]])
                cache.set(f'{room_name}code', self.code)
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


# 获取讲解信息
class ProductInfoView(APIView):
    def post(self, request):
        info = request.data.get("info")
        # 直播间名称
        room_name = request.data.get("room_name")
        # 款号
        code = next(iter(info.keys()))
        value = info[code]
        # 曝光量
        product_show_ucnt = value['add_product_show_ucnt']
        # 点击量
        product_click_ucnt = value['add_product_click_ucnt']
        # 销量
        pay_combo_cnt = value['add_pay_combo_cnt']
        # 总曝光人数
        room_live_exposure_sum = value['add_room_live_exposure_sum']
        # 总进入直播间人数
        in_room_live = value['add_in_room_live']
        # 点击率
        click_rate = value['click_rate']
        # 成交率
        success_reta = value['deal_rate']
        # 进入率
        in_live_rate = value['in_live_rate']

        # 讲解时间
        time = value['time']

        # 当前日期
        date_time = datetime.now().strftime("%Y-%m-%d")
        # 场次
        session = "第一场"

        # 结束时间
        s1 = datetime.now()
        s2 = timedelta(seconds=time)
        start_time = s1 - s2
        start_time = start_time.strftime("%Y-%m-%d %H:%M:%S")
        end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            productInfo = ProductInformation(
                code=code,
                room_name=room_name,
                date=date_time,
                exposure_count=product_show_ucnt,
                click_count=product_click_ucnt,
                total_exposure=room_live_exposure_sum,
                entry_count=in_room_live,
                live_time=time,
                click_rate=click_rate,
                success_reta=success_reta,
                in_live_rate=in_live_rate,
                pay_combo_cnt=pay_combo_cnt,
                session=session,
                start_time=start_time,
                end_time=end_time,
            )
            productInfo.save()
            return Response({'status': 'success'}, status=200)
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=500)

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
        queryset = ProductInformation.objects.filter(date=date_time, session=session, room_name=room_name)
        serializer = ProductInfoSerializer(queryset, many=True)
        return Response(serializer.data)


class LiveRoomDataView(APIView):
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
        room_name = request.query_params.get('room_name')
        # 根据获取的数据过滤查询集
        queryset = LiveRoomData.objects.filter(datetime__date=date_time, room_name=room_name)

        # 序列化查询集
        serializer = LiveRoomDataSerializer(queryset, many=True)

        # 返回响应
        return Response(serializer.data)

    def post(self, request):
        # 总曝光
        total_exposure = request.data.get("room_live_exposure_sum")
        # 进入直播间-广告
        enter_room_ad = request.data.get("enter_room_ad")
        # 点击商品-广告
        click_product_ad = request.data.get("click_product_ad")
        # 创建订单-广告
        create_order_ad = request.data.get("create_order_ad")
        # 成交订单-广告
        deal_order_ad = request.data.get("deal_order_ad")
        # 进入直播间-自然
        enter_room_organic = request.data.get("enter_room_organic")
        # 点击商品-自然
        click_product_organic = request.data.get("click_product_organic")
        # 创建订单-自然
        create_order_organic = request.data.get("create_order_organic")
        # 成交订单-自然
        deal_order_organic = request.data.get("deal_order_organic")
        # 商品序号
        product_sequence = request.data.get("product_sequence")
        # 商品款号
        product_code = request.data.get("product_code")

        # 商品曝光人数
        product_exposure_users = request.data.get("product_exposure_users")
        # 商品点击人数
        product_click_users = request.data.get("product_click_users")
        # 累计成交金额
        cumulative_deal_amount = int(request.data.get("cumulative_deal_amount"))
        # 累计成交订单数
        cumulative_deal_orders = request.data.get("cumulative_deal_orders")
        # 千川数据
        room_list = request.data.get("room_list")
        # 直播间名称
        room_name = request.data.get("room_name")

        matching_rooms = [room for room in room_list if room['product_id'] == int(product_sequence)][0]
        # 商品千次曝光成交
        product_ctr = matching_rooms["GPM"]
        # 广告结算订单数
        ad_settlement_orders = matching_rooms["order_number"]
        # 广告结算成本
        ad_settlement_cost = matching_rooms["order_rate"]
        # 点击成交转化率
        click_deal_conversion_rate = matching_rooms["clickDeal2"]

        # 广告成交订单数
        if float(matching_rooms["back_rate"]) != 0:
            ad_deal_orders = int(int(matching_rooms["order_number"]) / float(matching_rooms["back_rate"]))
        else:
            ad_deal_orders = int(matching_rooms["order_number"])

        # 销售金额
        salesPrice = matching_rooms["salesPrice"]
        # 销售件数
        salesNum = matching_rooms["salesNum"]
        # 单价
        if salesPrice != 0:
            price = salesPrice / salesNum
            # 广告GMV
            ad_gmv = ad_deal_orders * price
        else:
            ad_gmv = 0
        # 消耗
        expenditure = matching_rooms["GPM"]
        try:
            liveRoomData = LiveRoomData(
                total_exposure=total_exposure,
                enter_room_ad=enter_room_ad,
                click_product_ad=click_product_ad,
                create_order_ad=create_order_ad,
                deal_order_ad=deal_order_ad,
                enter_room_organic=enter_room_organic,
                click_product_organic=click_product_organic,
                create_order_organic=create_order_organic,
                deal_order_organic=deal_order_organic,
                product_sequence=product_sequence,
                product_code=product_code,
                ad_gmv=ad_gmv,
                expenditure=expenditure,
                product_ctr=product_ctr,
                ad_settlement_orders=ad_settlement_orders,
                ad_deal_orders=ad_deal_orders,
                ad_settlement_cost=ad_settlement_cost,
                click_deal_conversion_rate=click_deal_conversion_rate,
                product_exposure_users=product_exposure_users,
                product_click_users=product_click_users,
                cumulative_deal_amount=cumulative_deal_amount / 100,
                cumulative_deal_orders=cumulative_deal_orders,
                room_name=room_name
            )
            liveRoomData.save()
            return JsonResponse({'status': 'success'}, status=200)
        except Exception as e:
            error_message = traceback.format_exc()  # 获取异常信息的字符串形式
            return JsonResponse({'err': str(e)}, status=500)


def echarts1(request):
    room_name = request.GET.get("room_name")
    date_time = request.GET.get("date_time")
    queryset = LiveRoomData.objects.filter(room_name=room_name, datetime__date=date_time)
    data = list(queryset.values("product_code", "total_exposure", "enter_room_ad", "enter_room_organic",
                                "product_exposure_users", "product_click_users"))
    # 进入直播间 - 广告
    list1 = []
    live_code = ""
    li1 = []
    for index, item in enumerate(data[:-1]):
        if item["product_code"] != live_code:
            if len(li1) != 0:
                list1.append({live_code: li1})
            li1 = []
            live_code = item["product_code"]
        else:
            li1.append(data[index + 1]["enter_room_ad"] - item["enter_room_ad"])
    return JsonResponse({"list1": list1})


def echarts2(request):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d")

    room_name = request.GET.get("room_name")

    queryset = LiveRoomData.objects.filter(room_name=room_name, datetime__date=date_time)
    data = list(queryset.values("product_code", "total_exposure", "enter_room_ad", "enter_room_organic",
                                "product_exposure_users", "product_click_users"))
    # 进入直播间 - 自然
    list1 = []
    live_code = ""
    li1 = []
    enter_room_organic = 0
    old_enter_room_organic = 0
    count = 0
    for index, item in enumerate(data):
        if index == len(data) - 1:
            list1.append({live_code + ("(" + str(count + 1) + ")"): li1})
        if item["product_code"] != live_code:
            enter_room_organic = item["enter_room_organic"]
            if len(li1) != 0:
                for i in list1:
                    for key in i:
                        if live_code in key:
                            count += 1
                list1.append({live_code + ("(" + str(count+1) + ")"): li1})

            li1 = []
            live_code = item["product_code"]
        else:
            if item["enter_room_organic"] != old_enter_room_organic:
                li1.append(item["enter_room_organic"] - enter_room_organic)
                old_enter_room_organic = item["enter_room_organic"]
    return JsonResponse({"list1": list1})


def echarts3(request):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d")
    room_name = request.GET.get("room_name")
    search_code = request.GET.get("search_code")
    queryset = LiveRoomData.objects.filter(room_name=room_name, datetime__date=date_time)
    data = list(queryset.values("product_code", "total_exposure", "enter_room_ad", "enter_room_organic",
                                "product_exposure_users", "product_click_users"))
    # 曝光进入率
    list1 = {}
    live_code = ""
    list2 = []
    list3 = {}
    total_exposure = 0
    for item in data:
        if item["product_code"] != live_code:
            total_exposure = 0
            live_code = item["product_code"]
            list1[live_code] = []
            list3[live_code] = {"enter_room_ad_list": [],
                                "enter_room_organic_list": [],
                                "total_exposure_list": [], }
        else:
            if item["total_exposure"] != total_exposure:
                if item["total_exposure"] == 0:
                    item["total_exposure"] = 1
                exposure = (item["enter_room_ad"] + item["enter_room_organic"]) / item["total_exposure"]
                list1[live_code].append(exposure)
                list3[live_code]["total_exposure_list"].append(item["total_exposure"])
                list3[live_code]["enter_room_ad_list"].append(item["enter_room_ad"])
                list3[live_code]["enter_room_organic_list"].append(item["enter_room_organic"])
                total_exposure = item["total_exposure"]
    list2.append({search_code: list1[search_code]})
    chat_list = [0 for _ in range(len(list1[search_code]))]
    group_size = 2

    list4 = []
    item = list3[search_code]
    for i in range(0, len(item["total_exposure_list"]), group_size):
        group = item["total_exposure_list"][i:i + group_size]
        group2 = item["enter_room_ad_list"][i:i + group_size]
        group3 = item["enter_room_organic_list"][i:i + group_size]
        total_exposure = max(group) - min(group)
        enter_room_ad = max(group2) - min(group2)
        enter_room_organic = max(group3) - min(group3)
        total_exposure2 = enter_room_ad + enter_room_organic
        if total_exposure == 0:
            total_exposure = 1
        chat_list[i] = total_exposure2 / total_exposure
    list4.append({search_code: chat_list})
    return JsonResponse({"list1": list2, "list2": list4})


def echarts4(request):
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d")
    room_name = request.GET.get("room_name")
    search_code = request.GET.get("search_code")
    queryset = LiveRoomData.objects.filter(room_name=room_name, datetime__date=date_time)
    data = list(queryset.values("product_code", "total_exposure", "enter_room_ad", "enter_room_organic",
                                "product_exposure_users", "product_click_users"))
    # 曝光点击率
    list1 = {}
    live_code = ""
    list2 = []
    list3 = {}
    list4 = []
    for item in data:
        if item["product_code"] != live_code:
            live_code = item["product_code"]
            list1[live_code] = []
            list3[live_code] = {"product_click_users_list": [],
                                "product_exposure_users_list": []}
        else:
            if item["product_exposure_users"] == 0:
                item["product_exposure_users"] = 1
            exposure = item["product_click_users"] / item["product_exposure_users"]
            if exposure < 0.5:
                list3[live_code]["product_click_users_list"].append(item["product_click_users"])
                list3[live_code]["product_exposure_users_list"].append(item["product_exposure_users"])
                list1[live_code].append(exposure)

    list2.append({search_code: list1[search_code]})
    chat_list = [0 for _ in range(len(list1[search_code]))]
    group_size = 12
    item = list3[search_code]
    for i in range(0, len(item["product_click_users_list"]), group_size):
        group = item["product_click_users_list"][i:i + group_size]
        group2 = item["product_exposure_users_list"][i:i + group_size]
        product_click_users = max(group) - min(group)
        product_exposure_users = max(group2) - min(group2)
        if product_exposure_users == 0:
            product_exposure_users = 1
        chat_list[i] = product_click_users / product_exposure_users
    list4.append({search_code: chat_list})
    return JsonResponse({"list1": list2, "list2": list4})


def update_code(request):
    code = request.GET.get("code")
    img = request.GET.get("img")
    id = request.GET.get("id")
    number = request.GET.get("number")
    result = ", ".join([code, img, id, number])
    with open('clothing/static/code', mode="w", encoding="utf-8") as f:
        f.write(result)
    return HttpResponse("OK")


def get_code(request):
    with open('clothing/static/code', mode="r", encoding="utf-8") as f:
        code = f.read()
    item = code.split(",")
    result = {
        "code": item[0],
        "img": item[1],
        "id": item[2],
        "number": item[3],
    }
    return JsonResponse({"data": result})
