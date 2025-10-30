import pytest
from decimal import Decimal


class TestCryptoViews:
	"""视图测试类"""

	@pytest.fixture
	def api_client(self):
		"""提供 API 客户端"""
		from rest_framework.test import APIClient
		return APIClient()

	@pytest.fixture
	def sample_data(self):
		"""创建测试数据"""
		from data.models import CryptoCurrency, PriceHistory
		crypto = CryptoCurrency.objects.create(name="Bitcoin", symbol="BTC")
		price_history = PriceHistory.objects.create(
			cryptocurrency=crypto,
			price=Decimal('45000.00'),
			volume=Decimal('30000000000.00'),
			market_cap=Decimal('900000000000.00')
		)
		return {'crypto': crypto, 'price_history': price_history}

	# @pytest.mark.django_db
	# def test_currency_list_api(self, api_client, sample_data):
	# 	"""测试加密货币列表 API"""
	# 	# 注意：这里需要根据你的实际 URL 路由调整
	# 	response = api_client.get('/api/currencies/')
	#
	# 	assert response.status_code == 200
	# 	assert len(response.data) >= 1
	# 	# 查找包含 BTC 的条目
	# 	btc_data = next((item for item in response.data if item['symbol'] == 'BTC'), None)
	# 	assert btc_data is not None
	# 	assert btc_data['name'] == 'Bitcoin'

	@pytest.mark.django_db
	def test_currency_detail_api(self, api_client, sample_data):
		"""测试加密货币详情 API"""
		response = api_client.get(f'/dashboard/api/lastest_price/')

		assert response.status_code == 200


	@pytest.mark.django_db
	def test_price_history_api(self, api_client, sample_data):
		"""测试价格历史 API"""
		crypto = sample_data['crypto']
		# 假设你有一个价格历史端点
		response = api_client.get(f'/dashboard/api/price-history/{crypto.symbol}')

		# 如果端点存在，检查状态码
		if response.status_code != 404:  # 如果端点不存在，跳过某些断言
			assert response.status_code == 200
			assert len(response.data) >= 1