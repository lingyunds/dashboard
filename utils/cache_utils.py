import hashlib
from functools import wraps

from django.conf import settings
from django.core.cache import cache


class CacheHelper:
    """缓存工具类"""

    @staticmethod
    def generate_cache_key(prefix, *args, **kwargs):
        """
        生成统一的缓存键
        格式: crypto_dashboard:prefix:arg1:arg2:kwarg1=value1(dashboard后做hash)
        """
        key_parts = [prefix]

        # 添加位置参数
        for arg in args:
            key_parts.append(str(arg))

        # 添加关键字参数
        for key in sorted(kwargs.keys()):
            key_parts.append(f"{key}: {kwargs[key]}")

        # 生成哈希作为键
        key_string = ":".join(key_parts)
        return f"{settings.CACHES['default']['KEY_PREFIX']}: {hashlib.md5(key_string.encode()).hexdigest()}"

    @staticmethod
    def invalidate_pattern(pattern):
        """根据模式删除缓存键"""
        try:
            from django_redis import get_redis_connection

            redis_client = get_redis_connection("default")
            keys = redis_client.keys(pattern)
            if keys:
                redis_client.delete(*keys)
                return len(keys)
            return 0
        except Exception:
            return 0


def cached_method(timeout=300):
    """缓存方法结果的装饰器"""

    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            cache_key = CacheHelper.generate_cache_key(
                f"{self.__class__.__name__}.{method.__name__}", *args, **kwargs
            )

            result = cache.get(cache_key)
            if result is not None:
                return result

            result = method(self, *args, **kwargs)
            cache.set(cache_key, result, timeout)
            return result

        return wrapper

    return decorator
