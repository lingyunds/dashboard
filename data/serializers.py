from rest_framework import serializers
from .models import CryptoCurrency, PriceHistory
from typing import Dict, List, Optional

class PriceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceHistory
        fields = '__all__'

class CryptoCurrencySerializer(serializers.ModelSerializer):
    # 嵌套最新价格（通过ORM优化查询）
    #SerializerMethodField是Django REST framework提供的一个特殊字段类型，
    #它允许你定义一个方法来动态地获取和返回序列化数据中的某个字段值，这个方法可以根据模型实例的其他属性、关联模型或任何自定义的逻辑来生成返回值。
    latest_price = serializers.SerializerMethodField()

    class Meta:
        model = CryptoCurrency
        fields = ['id', 'name', 'symbol', 'latest_price']

    def get_latest_price(self, obj) -> Optional[float]:
        latest_entry = obj.price_history.first() # 因为Meta中定义了ordering，first()就是最新的
        return float(latest_entry.price) if latest_entry else None
