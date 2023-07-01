from rest_framework.pagination import PageNumberPagination


class OrderPagination(PageNumberPagination):
    """分页器"""
    page_size_query_param = "size"
    page_query_param = "page"