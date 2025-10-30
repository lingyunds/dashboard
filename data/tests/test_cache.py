import pytest
from django.core.cache import cache
from utils.cache_utils import CacheHelper, cached_method


class TestCacheUtils:
	"""缓存工具测试"""

	def setup_method(self):
		cache.clear()

	@pytest.mark.django_db
	def test_generate_cache_key(self):
		"""测试缓存键生成"""
		key1 = CacheHelper.generate_cache_key('test', 'arg1', param='value')
		key2 = CacheHelper.generate_cache_key('test', 'arg1', param='value')
		key3 = CacheHelper.generate_cache_key('test', 'arg2', param='value')

		assert key1 == key2
		assert key1 != key3
		assert 'crypto_dashboard' in key1

	@pytest.mark.django_db
	def test_cached_method_decorator(self):
		"""测试方法缓存装饰器"""

		class TestService:
			call_count = 0

			@cached_method(timeout=60)
			def expensive_operation(self, x):
				self.call_count += 1
				return x * 2

		service = TestService()

		# 第一次调用
		result1 = service.expensive_operation(5)
		assert result1 == 10
		assert service.call_count == 1

		# 第二次调用应该从缓存返回
		result2 = service.expensive_operation(5)
		assert result2 == 10
		assert service.call_count == 1