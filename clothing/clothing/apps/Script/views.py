import os
import re
import shutil
import http.client
import urllib.parse
import openai
from django.core.cache import cache
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Design, Tags, Size, Script, Collocation
from django.db import transaction, connection

from .serializers import DesignSerializer, TagsSerializer, SizeSerializer, ScriptSerializer, CollocationSerializer


# Create your views here.


class DesignView(APIView):
    def post(self, request):
        code_list = request.data.get("code_list")
        try:
            with transaction.atomic():
                inserted_count = 0
                for code in code_list:
                    is_exists = Design.objects.filter(code=code).exists()
                    if not is_exists:
                        insert_design(code)
                        inserted_count += 1
            return JsonResponse({'message': f'{inserted_count} 条数据更新成功。'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request):
        cart_codes = request.query_params.getlist("cart_codes[]")
        query_set = Design.objects.filter(code__in=cart_codes)
        serializer = DesignSerializer(instance=query_set, many=True)
        return JsonResponse({'message': serializer.data})


class TagsView(APIView):
    def get(self, request):
        design_id = request.query_params.get('design_id')
        query_set = Tags.objects.filter(design_id=design_id)
        serializer = TagsSerializer(instance=query_set, many=True)
        return JsonResponse({'message': serializer.data})

    def delete(self, request):
        # 删除不需要追踪的款号
        id = request.query_params.get('tag_id')
        try:
            Tags.objects.get(pk=id).delete()
            return JsonResponse({'message': '删除成功。'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request):
        name = request.data.get("name")
        design_id = request.data.get("design_id")
        try:
            tag = Tags.objects.create(design_id=design_id, tags=name)
            for i in range(3):
                Script.objects.create(tags=tag)
            serializer = TagsSerializer(instance=tag)
            return JsonResponse({'message': serializer.data})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)


class SizeView(APIView):
    def get(self, request):
        tags_id = request.query_params.get('tags_id')
        query_set = Size.objects.filter(tags_id=tags_id)
        serializer = SizeSerializer(instance=query_set, many=True)
        return JsonResponse({'message': serializer.data})

    def patch(self, request):
        id = request.data.get('tags_id')
        condition = request.data.get('condition')
        content = request.data.get('content')
        try:
            if condition == "size":
                Size.objects.filter(pk=id).update(size=content)
            if condition == "weight":
                Size.objects.filter(pk=id).update(weight=content)
            if condition == "height":
                Size.objects.filter(pk=id).update(height=content)
            return JsonResponse({'message': '更新成功。'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request):
        # 删除不需要追踪的款号
        id = request.query_params.get('size_id')
        try:
            Size.objects.get(pk=id).delete()
            return JsonResponse({'message': '删除成功。'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request):
        tags_id = request.data.get("tags_id")
        try:
            Size.objects.create(tags_id=tags_id)
            return JsonResponse({'message': '添加成功。'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class ScriptView(APIView):
    def get(self, request):
        tags_id = request.query_params.get('tags_id')
        query_set = Script.objects.filter(tags_id=tags_id)
        serializer = ScriptSerializer(instance=query_set, many=True)
        return JsonResponse({'message': serializer.data})

    def patch(self, request):
        id = request.data.get('id')
        original = request.data.get('original')
        gpt_original = request.data.get('gpt_original')
        try:
            Script.objects.filter(pk=id).update(original=original, gpt_original=gpt_original)
            return JsonResponse({'message': '更新成功。'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request):
        # 删除不需要追踪的款号
        id = request.query_params.get('id')
        try:
            Script.objects.get(pk=id).delete()
            return JsonResponse({'message': '删除成功。'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request):
        tags_id = request.data.get("tags_id")
        try:
            Script.objects.create(tags_id=tags_id)
            return JsonResponse({'message': '添加成功。'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)


def check_code(request, code):
    query = """
            SELECT
			MAX(g.merchant_name),
			SUM(CASE WHEN s.house='泰维仓' or s.house like '茉雅%%' or house ='公司搭配仓' THEN s.inventory ELSE 0 END) as inventory
			FROM
			taiwei_goods as g
			LEFT JOIN taiwei_stock as s
			ON g.merchant_code = s.code 
			WHERE g.merchant_code = %s
			GROUP BY g.merchant_code
			"""
    with connection.cursor() as cursor:
        cursor.execute(query, [code])
        result = cursor.fetchone()

    query2 = """
        SELECT
        SUM(live_deal_item_count),
        ROUND((SUM(live_deal_amount) / SUM(live_deal_item_count)),2) as price
        FROM
        taiwei_commodity
        WHERE commodity_title like %s
        GROUP BY commodity_title
        LIMIT 1
    """
    with connection.cursor() as cursor:
        cursor.execute(query2, ["%" + code[1:]])
        result2 = cursor.fetchone()

    query3 = """
        SELECT
        SUM(quantity)
        FROM
        taiwei_salesrecord
        WHERE product_code = %s
        GROUP BY product_code
    """
    with connection.cursor() as cursor:
        cursor.execute(query3, [code])
        result3 = cursor.fetchone()
    if not result2:
        price = "30天没卖过"
        live_deal_item_count = 0
    else:
        live_deal_item_count = result2[0]
        price = result2[1]
    if not result3:
        sales_quantity = 0
    else:
        sales_quantity = result3[0]

    if result:
        data = {"category": result[0], "inventory": result[1], 'live_deal_item_count': live_deal_item_count,
                'sales_quantity': sales_quantity, 'price': price}
        return JsonResponse(data)
    else:
        return JsonResponse({"data": "查询不到该商品信息"})


class CollocationView(APIView):
    def get(self, request):
        tags_id = request.query_params.get('tags_id')
        query_set = Collocation.objects.filter(tags_id=tags_id)
        serializer = CollocationSerializer(instance=query_set, many=True)
        return JsonResponse({'message': serializer.data})

    def patch(self, request):
        id = request.data.get('id')
        notes = request.data.get('notes')
        try:
            Collocation.objects.filter(pk=id).update(notes=notes)
            return JsonResponse({'message': '更新成功。'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def delete(self, request):
        # 删除不需要追踪的款号
        id = request.query_params.get('id')
        file_name = request.query_params.get('file_name')
        try:
            Collocation.objects.filter(pk=id).delete()
            path = 'Y:/'

            # 构建目标路径
            target_path = 'X:/' + file_name

            # 移动文件
            shutil.move(os.path.join(path, file_name), target_path)
            return JsonResponse({'message': '删除成功。'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request):
        tags_id = request.data.get("tags_id")
        design_code = request.data.get("design_code")
        path = 'Y:/'
        pattern = r'[a-z]+\d+'
        collocation_list = []
        for filename in os.listdir(path):
            if design_code in filename.lower():
                is_exists = Collocation.objects.filter(codes=filename, tags_id=tags_id).exists()
                if is_exists:
                    continue
                matching_filenames = []
                # 找到所有匹配的模式
                matches = re.findall(pattern, filename, re.IGNORECASE)
                matching_filenames.extend(matches)
                collocation = Collocation(
                    codes=filename,
                    notes='',
                    tags_id=tags_id,
                    child_code=",".join(matching_filenames)
                )
                collocation_list.append(collocation)
        try:
            Collocation.objects.bulk_create(collocation_list)
            return JsonResponse({'message': '添加成功。'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


openai.api_key = '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'


def reply(request):
    try:
        content = request.GET.get("content")

        messages = [{
            "role": "system",
            "content": '''帮我润色加工一下这句话，让产品看起来更有信任感和吸引力，产品类目是女装，文字适合口语，让消费者有购买的理由和冲动，可以展开2到3个方面讲，总的字数控制稍微简洁些，记得要口语化'''
        },
            {"role": "user", "content": content}, ]

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        result = response['choices'][0]['message']['content']

        response_data = {'result': result}
        return JsonResponse(response_data)
    except Exception as e:
        print(e)
        return JsonResponse({'error': str(e)}, status=500)


def context_reply(request):
    content = request.GET.get("content")
    messages = cache.get('messages', [])
    messages.append({"role": "user", "content": content})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    result = response['choices'][0]['message']['content']

    messages.append({"role": "assistant", "content": result})
    cache.set("messages", messages[-3:])
    response_data = {'result': result}
    return JsonResponse(response_data)


class DesignDetailView(APIView):
    def get(self, request, *args, **kwargs):
        code = request.query_params.get('code')

        # 获取所有具有特定 code 的 Design 对象
        designs = Design.objects.filter(code__contains=code)
        if not designs:
            return Response([])
        # 初始化一个空列表，用于保存所有设计的数据
        designs_data = []

        # 遍历每一个 Design 对象
        for design in designs:
            # 获取与该 Design 对象相关联的所有 Tags 对象
            tags = design.tags.all()

            # 所有关联对象的列表
            related_data = []

            # 遍历每一个 Tag 对象
            for tag in tags:
                related_data.append({
                    "tag": tag.tags,
                    "tag_id": tag.id,
                    "tag_notes": tag.notes,
                    "child": {
                        "sizes": [{"size": size.size, "weight": size.weight, "height": size.height} for size in
                                  tag.size.all()],
                        "scripts": [
                            {"script_id": script.id, "original": script.original, "gpt_original": script.gpt_original}
                            for script in tag.script.all()],
                        "collocations": [{"codes": collocation.codes, "notes": collocation.notes} for collocation in
                                         tag.collocation.all()],
                    }
                })

            # 保存当前设计的数据
            designs_data.append({
                "id": design.id,
                "code": design.code,
                "name": design.name,
                "designer": design.designer,
                "material": design.material,
                "specification_quantity": design.specification_quantity,
                "child": related_data
            })

        # 返回所有设计的数据
        return JsonResponse(designs_data, safe=False)


def processGETRequest(request):
    text = request.GET.get("text")
    appKey = 'vGCdB1HewZ252IqX'
    token = '427a48268b244196b9314e37d61e025f'
    text = urllib.parse.quote_plus(text)
    text = text.replace("+", "%20")
    text = text.replace("*", "%2A")
    text = text.replace("%7E", "~")
    audioSaveFile = 'clothing/static/syAudio.wav'
    format = 'wav'
    sampleRate = 16000
    host = 'nls-gateway-cn-shanghai.aliyuncs.com'
    url = 'https://' + host + '/stream/v1/tts'
    # 设置URL请求参数
    url = url + '?appkey=' + appKey
    url = url + '&token=' + token
    url = url + '&text=' + text
    url = url + '&format=' + format
    url = url + '&sample_rate=' + str(sampleRate)
    # voice 发音人，可选，默认是xiaoyun。
    url = url + '&voice=' + 'voice-cdac47e'
    # volume 音量，范围是0~100，可选，默认50。
    # url = url + '&volume=' + str(50)
    # speech_rate 语速，范围是-500~500，可选，默认是0。
    # url = url + '&speech_rate=' + str(0)
    # pitch_rate 语调，范围是-500~500，可选，默认是0。
    # url = url + '&pitch_rate=' + str(0)
    conn = http.client.HTTPSConnection(host)
    conn.request(method='GET', url=url)
    # 处理服务端返回的响应。
    response = conn.getresponse()
    contentType = response.getheader('Content-Type')
    body = response.read()
    if 'audio/mpeg' == contentType:
        with open(audioSaveFile, mode='wb') as f:
            f.write(body)
    else:
        print('The GET request failed: ' + str(body))
    conn.close()
    return HttpResponse("OK")


def insert_design(code):
    query = """
                INSERT INTO taiwei_design
                (code,name,designer,material,specification_quantity)
                SELECT
                merchant_code,
                merchant_name,
                (SELECT designer FROM taiwei_new_style WHERE code = merchant_code LIMIT 1) as designer,
                season,
                (
                    SELECT GROUP_CONCAT(workshop SEPARATOR '  ')
                    FROM (
                            SELECT CONCAT(cls, '-', SUM(CASE WHEN house like "泰维仓" or house like "茉雅%%" THEN inventory ELSE 0 END)) AS workshop
                            FROM taiwei_newstock
                            WHERE code = merchant_code
                            GROUP BY code, cls
                    ) AS subquery
            ) AS specification_quantity
                FROM
                taiwei_goods
                WHERE merchant_code = %s    
            """
    with connection.cursor() as cursor:
        cursor.execute(query, [code])
        design_id = cursor.lastrowid
        tags_query = "INSERT INTO taiwei_design_tags (tags, design_id) VALUES (%s, %s)"
        for tag in ["版型", "设计", "工艺", "材质", "尺码", "搭配"]:
            tags_data = (tag, design_id)
            cursor.execute(tags_query, tags_data)
            # 获取插入的 tags 记录的主键 id
            tags_id = cursor.lastrowid
            if tag == "尺码":
                # 插入 taiwei_design_size 数据
                size_query = """
                                        INSERT INTO 
                                        taiwei_design_size (size, weight, height, tags_id) 
                                        VALUES (%s, %s, %s, %s)"""
                size_data = ("M", 80, 160, tags_id)
                cursor.execute(size_query, size_data)
            for j in range(3):
                script_query = """
                                        INSERT INTO 
                                        taiwei_design_script 
                                        (original, gpt_original, tags_id) 
                                        VALUES (%s, %s, %s)"""

                script_data = (None, None, tags_id)
                cursor.execute(script_query, script_data)


class Design2View(APIView):
    def post(self, request):
        path = 'W:/'
        pattern = r'[a-z]+\d+'
        codes = set()
        for filename in os.listdir(path):
            if filename == 'Thumbs.db':
                continue  # 忽略 Thumbs.db
            matching_filenames = []
            # 找到所有匹配的模式
            matches = re.findall(pattern, filename, re.IGNORECASE)
            codes.update(matches)
            matching_filenames.extend(matches)
        try:
            with transaction.atomic():
                inserted_count = 0
                for code in codes:
                    if len(code) != 4:
                        continue
                    is_exists = Design.objects.filter(code=code).exists()
                    if not is_exists:
                        try:
                            insert_design(code)
                        except Exception as e:
                            continue
                        inserted_count += 1
            return JsonResponse({'message': f'{inserted_count} 条数据更新成功。'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request):
        search_code = request.GET.get('code')
        path = 'W:/'
        if search_code:
            path = "Y:/"
        pattern = r'[a-z]+\d+'
        data = {}
        codes = set()
        for filename in os.listdir(path):
            if filename == 'Thumbs.db':
                continue  # 忽略 Thumbs.db
            if search_code and search_code not in filename.lower():
                continue
            # 找到所有匹配的模式
            matches = re.findall(pattern, filename, re.IGNORECASE)
            codes.update(matches)
            design_data = []
            for code in matches:
                try:
                    if search_code:
                        design_info = {"code": code}
                        design_data.append(design_info)
                    else:
                        design = Design.objects.get(code=code)
                        tags_list = [{'id': tag.id, 'tags': tag.tags, "notes": tag.notes} for tag in design.tags.all()]
                        design_info = {"id": design.id, "code": code, "tags": tags_list}
                        design_data.append(design_info)
                except Exception as e:
                    continue
            data[filename] = {"design_data": design_data, "checked": False}
        return JsonResponse({"data": data, "code_list": list(codes)}, safe=False)


def show_design4(request):
    type = request.GET.get('type')
    name = request.GET.get('name')
    path = 'U:/'
    if name == 'yijia':
        if type == '2':
            path = 'R:/'
        else:
            path = 'S:/'
    if name == 'xj':
        if type == '2':
            path = 'P:/'
        else:
            path = 'Q:/'
    if name == 'yy':
        if type == '2':
            path = 'N:/'
        else:
            path = 'O:/'
    if name != "yijia" and name != "xj" and name != "yy":
        if type == '2':
            path = 'T:/'
        else:
            path = 'U:/'

    pattern = r'[a-z]+\d+'
    data = {}
    codes = set()
    for filename in os.listdir(path):
        if filename == 'Thumbs.db':
            continue  # 忽略 Thumbs.db
        # 找到所有匹配的模式
        matches = re.findall(pattern, filename, re.IGNORECASE)
        codes.update(matches)
        design_data = []
        for code in matches:
            design_info = {"code": code}
            design_data.append(design_info)
        data[filename] = {"design_data": design_data}
    return JsonResponse({"data": data, "code_list": list(codes)}, safe=False)


def del_img(request):
    try:
        name = request.GET.get('name')
        type = request.GET.get('type')
        user_name = request.GET.get('user_name')
        path = 'U:/'
        if user_name == 'yijia':
            if type == '2':
                path = 'R:/'
            else:
                path = 'S:/'
        if user_name == 'xj':
            if type == '2':
                path = 'P:/'
            else:
                path = 'Q:/'
        if user_name == 'yy':
            if type == '2':
                path = 'N:/'
            else:
                path = 'O:/'
        if user_name != "yijia" and user_name != "xj" and user_name != 'yy':
            if type == '2':
                path = 'T:/'
            else:
                path = 'U:/'
        file_name = path + name
        os.remove(file_name)
        return JsonResponse({"message": "删除成功"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": "删除失败"}, status=500)


def export_code(request):
    name = request.GET.get("name")
    type = request.GET.get("type")
    path = 'U:/'
    if name == 'yijia':
        if type == '2':
            path = 'R:/'
        else:
            path = 'S:/'
    if name == 'xj':
        if type == '2':
            path = 'P:/'
        else:
            path = 'Q:/'
    if name == 'yy':
        if type == '2':
            path = 'N:/'
        else:
            path = 'O:/'
    if name != "yijia" and name != "xj" and name != "yy":
        if type == '2':
            path = 'T:/'
        else:
            path = 'U:/'
    filename_list = []
    for filename in os.listdir(path):
        if filename == 'Thumbs.db':
            continue  # 忽略 Thumbs.db
        name, _ = os.path.splitext(filename)  # 获取文件名，忽略扩展名
        filename_list.append(name)
    return JsonResponse({"data": filename_list}, safe=False)


def update_notes(request):
    id = request.GET.get("id")
    notes = request.GET.get("notes")
    try:
        Tags.objects.filter(pk=id).update(notes=notes)
        return JsonResponse({"message": "更新成功"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": "更新失败"}, status=500)


def get_designer(request):
    query = "SELECT DISTINCT designer FROM `taiwei_new_style` WHERE designer is not null"
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    designer_list = []
    for item in result:
        designer_list.append(item[0])
    return JsonResponse({"message": designer_list}, safe=False)


class DesignerView(APIView):
    def post(self, request):
        inserted_count = 0
        time_count = request.data.get("time_count")
        designer = request.data.get("designer")
        query = """
        SELECT DISTINCT code FROM `taiwei_new_style` 
        WHERE YEAR(date) = YEAR(CURDATE()) AND MONTH(date) = %s AND designer=%s
        """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, [time_count, designer])
                result = cursor.fetchall()
            for item in result:
                code = item[0]
                is_exists = Design.objects.filter(code=code).exists()
                if not is_exists:
                    try:
                        insert_design(code)
                    except Exception as e:
                        continue
                    inserted_count += 1
            return JsonResponse({'message': f'{inserted_count} 条数据更新成功。'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request):
        time_count = request.query_params.get("time_count")
        designer = request.query_params.get("designer")
        where_list = [time_count, designer]
        query = """
        SELECT DISTINCT code FROM `taiwei_new_style` 
        WHERE YEAR(date) = YEAR(CURDATE()) AND MONTH(date) = %s AND designer=%s
        """
        if time_count == "加急":
            where_list = [designer]
            query = """
            SELECT DISTINCT code FROM `taiwei_new_style` 
            WHERE designer=%s 
            AND code in (SELECT DISTINCT commodity_code FROM taiwei_product where cart_name = '星露购物车')
            """
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, where_list)
                result = cursor.fetchall()
                code_list = []
                for item in result:
                    code_list.append(item[0])
            return JsonResponse({'message': code_list}, safe=False)
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)


def get_code_info(request):
    code = request.GET.get("code")
    notes = ''
    tag_id = ''
    design = Design.objects.filter(code=code).first()
    if design:
        tags = design.tags.all()
        # 这将会打印所有与此design相关的标签
        for tag in tags:
            if tag.tags == '版型':
                notes = tag.notes
                tag_id = tag.id
    return JsonResponse({'message': {"code": code, "notes": notes, "tag_id": tag_id}}, safe=False)


def get_search_code(request):
    code = request.GET.get("code")
    query = f"SELECT code FROM taiwei_new_style WHERE code like '%{code}%'"
    code_list = []
    with connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    for item in result:
        code = item[0]
        code_list.append(code)
        is_exists = Design.objects.filter(code=code).exists()
        if not is_exists:
            try:
                insert_design(code)
            except Exception as e:
                continue
    return JsonResponse({'message': code_list}, safe=False)
