from django.shortcuts import render

from django.db import connection

from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView

from .models import DouyinUser
from clothing.util.getGood import get_douyin_user


def get_user_name(request):
    code = request.GET.get('code')
    query = f"""
        SELECT
        u.name
        FROM
        taiwei_orders as o
        LEFT JOIN taiwei_user as u
        ON o.sub_order_no = u.sub_order_no
        WHERE DATE(o.order_submit_time) >= CURDATE() - INTERVAL 30 DAY
        AND o.merchant_code LIKE '%{code}%'
        AND u.name is not null
    """
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    user_list = []
    for i in result:
        user_list.append(i[0])
    return JsonResponse({"data": user_list})


class douYinUser(APIView):
    def post(self, request):
        user_info = request.data
        douyin_list = []
        for item in user_info:
            douyin = DouyinUser(
                douyin_id=item['douyin_id'],
                is_fan_group=item['is_fan_group'],
                style_number=item['style_number'],
                time=item['time'],
                username=item['username'],
            )
            douyin_list.append(douyin)

        try:
            inserted_count = DouyinUser.objects.bulk_create(douyin_list)
            return JsonResponse({'message': f'{len(inserted_count)} 条数据更新成功。'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


def get_live_douyin_user(request):
    response = get_douyin_user()
    return JsonResponse({'message': response})
