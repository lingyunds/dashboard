#!/usr/bin/env python
# -*- coding: utf-8 -*-


from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    """分页器类"""

    page_size = 20  # 默认每页返回的条数
    page_query_param = "page"  # url中设置 page 的键,默认为page
    page_size_query_param = "page_size"  # url中设置 page_size 的键,默认为None
    max_page_size = 2000  # 每页返回的最大条数，默认为None
