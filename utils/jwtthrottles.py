#! usr bin env python
# -*- coding: utf-8 -*-
from rest_framework.throttling import SimpleRateThrottle


class AllThrottle(SimpleRateThrottle):
    scope = "all"

    def get_cache_key(self, request, view):
        token = request.META.get("HTTP_AUTHORIZATION")
        # 没有登录根据ip限制
        if not token:
            token = request.META.get("HTTP_HOST")
        return "throttle_%(scope)s_%(ident)s" % {"scope": self.scope, "ident": token}
