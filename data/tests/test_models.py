import time

import pytest
from decimal import Decimal
from data.models import CryptoCurrency, PriceHistory


class TestCryptoCurrencyModel:
	"""加密货币模型测试类"""

	@pytest.mark.django_db
	def test_create_cryptocurrency(self):
		"""测试创建加密货币模型"""
		crypto = CryptoCurrency.objects.create(
			name="Bitcoin",
			symbol="BTC"
		)
		assert crypto.name == "Bitcoin"
		assert crypto.symbol == "BTC"
		assert str(crypto) == "Bitcoin (BTC)"

	@pytest.mark.django_db
	def test_unique_symbol_constraint(self):
		"""测试符号唯一性约束"""
		CryptoCurrency.objects.create(name="Bitcoin", symbol="BTC")
		with pytest.raises(Exception):  # 可能是 IntegrityError
			CryptoCurrency.objects.create(name="Bitcoin Cash", symbol="BTC")

	@pytest.mark.django_db
	def test_symbol_max_length(self):
		"""测试符号字段的最大长度"""
		crypto = CryptoCurrency.objects.create(
			name="Test Coin",
			symbol="TEST12345"  # 10个字符，应该符合 max_length=10
		)
		assert len(crypto.symbol) == 9


class TestPriceHistoryModel:
	"""价格历史模型测试类"""

	@pytest.fixture
	def crypto(self):
		"""创建测试用的加密货币"""
		return CryptoCurrency.objects.create(name="Bitcoin", symbol="BTC")

	@pytest.mark.django_db
	def test_create_price_history(self, crypto):
		"""测试创建价格历史记录"""
		price_history = PriceHistory.objects.create(
			cryptocurrency=crypto,
			price=Decimal('45000.50'),
			volume=Decimal('30000000000.00'),
			market_cap=Decimal('900000000000.00')
		)

		assert price_history.cryptocurrency == crypto
		assert price_history.price == Decimal('45000.50')
		assert "BTC - $45000.50" in str(price_history)

	@pytest.mark.django_db
	def test_price_history_ordering(self, crypto):
		"""测试价格历史记录的排序"""
		# 创建多个价格记录
		PriceHistory.objects.create(
			cryptocurrency=crypto, price=Decimal('40000.00')
		)
		time.sleep(0.1) # 内存数据库操作保证不了先后顺序
		PriceHistory.objects.create(
			cryptocurrency=crypto, price=Decimal('45000.00')
		)
		time.sleep(0.1)
		PriceHistory.objects.create(
			cryptocurrency=crypto, price=Decimal('42000.00')
		)

		# 获取最新记录（应该按时间降序）
		latest = PriceHistory.objects.first()
		assert latest.price == Decimal('42000.00')