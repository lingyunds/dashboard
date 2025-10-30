from rest_framework import viewsets
from .models import CryptoCurrency, PriceHistory
from .serializers import CryptoCurrencySerializer, PriceHistorySerializer
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from utils.cache_utils import CacheHelper


class CurrencyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API端点：列出所有加密货币及其最新价格。
    """
    queryset = CryptoCurrency.objects.all().prefetch_related('price_history')
    serializer_class = CryptoCurrencySerializer

    @method_decorator(cache_page(60 * 5))  # 缓存5分钟
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PriceHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PriceHistory.objects.all()
    serializer_class = PriceHistorySerializer

    def list(self, request, symbol, *args, **kwargs):
        # symbol = self.request.query_params.get('symbol')

        cache_key = CacheHelper.generate_cache_key(f'currency_price_history_{symbol}',request.get_full_path())
        cached_data = cache.get(cache_key)
        if cached_data is not None:
            return Response(cached_data)

        queryset = self.get_queryset().filter(cryptocurrency__symbol=symbol)[:50]

        serializer = self.get_serializer(queryset, many=True)
        # 缓存5分钟
        cache.set(cache_key, serializer.data, 300)

        return Response(serializer.data)