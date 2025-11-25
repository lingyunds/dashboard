from typing import List, Tuple

from django.db import models


# Create your models here.
class CryptoCurrency(models.Model):
    name = models.CharField(max_length=100)  # e.g., Bitcion
    symbol = models.CharField(max_length=10, unique=True)  # e.g., BTC
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.symbol})"


class PriceHistory(models.Model):
    cryptocurrency = models.ForeignKey(
        CryptoCurrency, on_delete=models.CASCADE, related_name="price_history"
    )  # 一对多需级联删除
    price = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)  # 交易量
    market_cap = models.DecimalField(max_digits=30, decimal_places=2, null=True, blank=True)  # 市值
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]  # 默认按时间降序排列，方便获取最新数据

    def __str__(self) -> str:
        return f"{self.cryptocurrency.symbol} - ${self.price} at {self.timestamp}"
