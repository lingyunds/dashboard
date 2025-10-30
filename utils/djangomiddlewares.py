#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.middleware.common import MiddlewareMixin


class GlobalExceptionMiddleware(MiddlewareMixin):
    """统一异常处理中间件"""

    def process_exception(self, request, exception):
        # 直接抛出 django admin 的异常
        if str(request.path).startswith("/admin/"):
            return None
        # 捕获其他异常，直接返回 500
        return HttpResponse(exception)
