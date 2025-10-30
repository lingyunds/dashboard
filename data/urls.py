#!/usr/bin/env python
# -*- coding: utf-8 -*-
# products/urls.py

from django.urls import re_path
from .views import CurrencyViewSet,PriceHistoryViewSet

lastest_price = CurrencyViewSet.as_view({
    'get': 'list',
})

price_history = PriceHistoryViewSet.as_view({
    'get': 'list',
})


urlpatterns = [
	re_path(r'^lastest_price/$', lastest_price),
	re_path(r'^price_history/(?P<symbol>.*)/$', price_history),

]
