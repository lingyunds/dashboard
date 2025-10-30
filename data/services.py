from typing import Dict, List, Optional

import requests
from django.db import transaction

from utils.cache_utils import CacheHelper, cached_method

from .models import CryptoCurrency, PriceHistory


class CryptoDataService:
    API_URL = "https://api.coingecko.com/api/v3/simple/price"

    # 映射加密货币符号到 CoinGecko ID
    COIN_MAPPING = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "BNB": "binancecoin",
        "ADA": "cardano",
        "XRP": "ripple",
        "DOT": "polkadot",
        "LTC": "litecoin",
        "LINK": "chainlink",
        # 你可以添加更多映射
    }

    @staticmethod
    def fetch_crypto_data(symbols: List[str]) -> Optional[List[Dict]]:
        """
        从API获取加密货币数据
        """

        try:
            # 将符号转换为 CoinGecko ID
            coin_ids = [
                CryptoDataService.COIN_MAPPING[symbol]
                for symbol in symbols
                if symbol in CryptoDataService.COIN_MAPPING
            ]
            if not coin_ids:
                return None

            # 将 ID 列表转换为逗号分隔的字符串
            ids_param = ",".join(coin_ids)

            params = {
                "ids": ids_param,
                "vs_currencies": "usd",
                "include_market_cap": "true",
                "include_24hr_vol": "true",
                "x_cg_demo_api_key": "CG-88HeSxFzeErxbX3fXXHscoXm",
            }
            response = requests.get(CryptoDataService.API_URL, params=params, timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            return response.json()
        except Exception as e:
            # 这里应该使用日志记录错误，而不是print
            print(f"Error fetching data: {e}")
            return None

    @staticmethod
    @transaction.atomic
    def update_database(api_data: Dict) -> None:
        """
        解析API数据并更新数据库
        {'bitcoin': {'usd': 109305, 'usd_market_cap': 2181482125001.7085, 'usd_24h_vol': 73721844216.49341},
        'ethereum': {'usd': 3872.05, 'usd_market_cap': 467936552076.28204, 'usd_24h_vol': 39215870683.11749}}
        """
        # 反转映射，从 ID 到符号
        symbol_mapping = {v: k for k, v in CryptoDataService.COIN_MAPPING.items()}

        for coin_id, data in api_data.items():
            symbol = symbol_mapping.get(coin_id)
            if not symbol:
                continue

            crypto, created = CryptoCurrency.objects.get_or_create(
                symbol=symbol, defaults={"name": coin_id.title()}
            )
            # 创建新的价格记录
            PriceHistory.objects.create(
                cryptocurrency=crypto,
                price=data["usd"],
                market_cap=data.get("usd_market_cap"),
                volume=data.get("usd_24h_vol"),
            )

        # 数据更新后，使相关缓存失效
        CacheHelper.invalidate_pattern("*crypto_dashboard*")

    # @cached_method方法装饰器示例
    #
    # @classmethod
    # @cached_method(timeout=120)  # 缓存2分钟
    # def get_latest_prices(cls, symbols: List[str]) -> Dict:
    #     """获取最新价格，使用缓存优化数据库查询"""
    #     prices = {}
    #     for symbol in symbols:
    #         try:
    #             crypto = CryptoCurrency.objects.get(symbol=symbol)
    #             latest_price = crypto.price_history.first()
    #             if latest_price:
    #                 prices[symbol] = {
    #                     'price': float(latest_price.price),
    #                     'timestamp': latest_price.timestamp.isoformat(),
    #                     'market_cap': float(latest_price.market_cap) if latest_price.market_cap else None,
    #                 }
    #         except CryptoCurrency.DoesNotExist:
    #             continue
    #
    #     return prices
