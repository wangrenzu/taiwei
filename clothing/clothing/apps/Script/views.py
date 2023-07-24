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
        cart_name = request.data.get("cart_name")
        try:
            with transaction.atomic():
                inserted_count = 0
                for code in code_list:
                    is_exists = Design.objects.filter(code=code, cart_name=cart_name).exists()
                    if not is_exists:
                        query = """
                            INSERT INTO taiwei_design
                            (code,name,designer,material,specification_quantity,cart_name)
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
                        ) AS specification_quantity,
                        %s as cart_name
                            FROM
                            taiwei_goods
                            WHERE merchant_code = %s    
                        """
                        with connection.cursor() as cursor:
                            cursor.execute(query, [cart_name, code])
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
                                if tag == "搭配":
                                    collocation_query = "INSERT INTO taiwei_design_collocation (codes,notes, tags_id) VALUES (%s,%s, %s)"
                                    collocation_data = (code, None, tags_id)
                                    cursor.execute(collocation_query, collocation_data)
                            inserted_count += 1
            return JsonResponse({'message': f'{inserted_count} 条数据更新成功。'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request):
        cart_name = request.query_params.get('cart_name')
        query_set = Design.objects.filter(cart_name=cart_name)
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
        print(id, condition, content)
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
			SUM(CASE WHEN s.house='泰维仓' or s.house like '茉雅%%' THEN s.inventory ELSE 0 END) as inventory
			FROM
			taiwei_goods as g
			LEFT JOIN taiwei_stock as s
			ON g.merchant_code = s.code 
			WHERE g.merchant_code = %s
			GROUP BY g.merchant_code
			"""
    data = "查询不到该商品信息"
    with connection.cursor() as cursor:
        cursor.execute(query, [code])
        result = cursor.fetchone()
    if result:
        data = f"{result[0]} {result[1]}"
    return HttpResponse(data)


class CollocationView(APIView):
    def get(self, request):
        tags_id = request.query_params.get('tags_id')
        query_set = Collocation.objects.filter(tags_id=tags_id)
        serializer = CollocationSerializer(instance=query_set, many=True)
        return JsonResponse({'message': serializer.data})

    def patch(self, request):
        id = request.data.get('id')
        codes = request.data.get('codes')
        notes = request.data.get('notes')
        if len(codes) == 0:
            Collocation.objects.get(pk=id).delete()
        try:
            Collocation.objects.filter(pk=id).update(codes=codes, notes=notes)
            return JsonResponse({'message': '更新成功。'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request):
        tags_id = request.data.get("tags_id")
        design_code = request.data.get("design_code")
        try:
            Collocation.objects.create(tags_id=tags_id, codes=design_code)
            return JsonResponse({'message': '添加成功。'})
        except Exception as e:
            print(e)
            return JsonResponse({'error': str(e)}, status=500)


openai.api_key = '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'


def reply(request):
    content = request.GET.get("content")

    messages = [{
        "role": "system",
        "content": '''帮我加工一下这段话'''
    },
        {"role": "user", "content": content}, ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
    )

    result = response['choices'][0]['message']['content']

    response_data = {'result': result}
    return JsonResponse(response_data)


def context_reply(request):
    content = request.GET.get("content")
    messages = cache.get('messages', [])
    messages.append({"role": "user", "content": content})
    print(messages)
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
                    "child": {
                        "sizes": [{"size": size.size, "weight": size.weight, "height": size.height} for size in
                                  tag.size.all()],
                        "scripts": [
                            {"original": script.original, "gpt_original": script.gpt_original}
                            for script in tag.script.all()],
                        "collocations": [{"codes": collocation.codes, "notes": collocation.notes} for collocation in
                                         tag.collocation.all()],
                    }
                })

            # 保存当前设计的数据
            designs_data.append({
                "code": design.code,
                "name": design.name,
                "designer": design.designer,
                "material": design.material,
                "specification_quantity": design.specification_quantity,
                "cart_name": design.cart_name,
                "child": related_data
            })

        # 返回所有设计的数据
        return JsonResponse(designs_data, safe=False)

