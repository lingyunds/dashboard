import pytest
from unittest.mock import patch, MagicMock
from data.services import CryptoDataService
from data.models import CryptoCurrency, PriceHistory


class TestCryptoDataService:
	"""加密货币数据服务测试类"""

	@pytest.fixture(autouse=True)
	def setup(self):
		"""每个测试前的设置"""
		self.btc = CryptoCurrency.objects.create(name="Bitcoin", symbol="BTC")
		self.eth = CryptoCurrency.objects.create(name="Ethereum", symbol="ETH")

	@pytest.mark.django_db
	def test_coin_mapping_exists(self):
		"""测试币种映射是否存在"""
		assert 'BTC' in CryptoDataService.COIN_MAPPING
		assert 'ETH' in CryptoDataService.COIN_MAPPING
		assert CryptoDataService.COIN_MAPPING['BTC'] == 'bitcoin'

	@pytest.mark.django_db
	@patch('data.services.requests.get')
	def test_fetch_crypto_data_success(self, mock_get):
		"""测试成功获取加密货币数据"""
		# 模拟成功的 API 响应
		mock_response = MagicMock()
		mock_response.json.return_value = {
			'bitcoin': {
				'usd': 45000.50,
				'usd_market_cap': 900000000000.00,
				'usd_24h_vol': 30000000000.00
			}
		}
		mock_response.raise_for_status.return_value = None
		mock_get.return_value = mock_response

		result = CryptoDataService.fetch_crypto_data(['BTC'])

		assert result is not None
		assert 'bitcoin' in result
		assert result['bitcoin']['usd'] == 45000.50
		mock_get.assert_called_once()

	@pytest.mark.django_db
	@patch('data.services.requests.get')
	def test_fetch_crypto_data_timeout(self, mock_get):
		"""测试 API 超时情况"""
		mock_get.side_effect = ConnectionError("Connection timeout")

		result = CryptoDataService.fetch_crypto_data(['BTC'])

		assert result is None

	@pytest.mark.django_db
	def test_update_database_creates_records(self):
		"""测试数据库更新创建新记录"""
		api_data = {
			'bitcoin': {
				'usd': 45000.50,
				'usd_market_cap': 900000000000.00,
				'usd_24h_vol': 30000000000.00
			}
		}

		# 初始记录数
		initial_count = PriceHistory.objects.count()

		# 调用更新数据库
		CryptoDataService.update_database(api_data)

		# 验证新记录被创建
		assert PriceHistory.objects.count() == initial_count + 1

		latest_price = PriceHistory.objects.filter(cryptocurrency=self.btc).first()
		assert float(latest_price.price) == 45000.50
		assert float(latest_price.market_cap) == 900000000000.00

	@pytest.mark.django_db
	@pytest.mark.parametrize("api_data,expected_count", [
		({'bitcoin': {'usd': 45000.50}}, 1),
		({'bitcoin': {'usd': 45000.50}, 'ethereum': {'usd': 3000.75}}, 2),
		({}, 0),
	])
	def test_update_database_various_scenarios(self, api_data, expected_count):
		"""测试数据库更新的各种场景"""
		initial_count = PriceHistory.objects.count()
		CryptoDataService.update_database(api_data)
		assert PriceHistory.objects.count() == initial_count + expected_count