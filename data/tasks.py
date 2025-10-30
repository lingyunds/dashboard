from celery import shared_task
from celery.utils.log import get_task_logger

from .services import CryptoDataService

# 获取 Celery 任务的日志器
logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3)
def update_crypto_prices(self):
    """
    Celery 任务：获取并更新加密货币价格
    使用 bind=True 允许我们访问任务实例（self）
    max_retries=3 表示任务失败时最多重试3次
    """
    try:
        logger.info("开始更新加密货币价格...")

        # 定义要跟踪的加密货币符号
        symbols = ["BTC", "ETH", "BNB", "ADA", "XRP", "DOT", "LTC", "LINK"]

        # 调用服务层获取数据
        data = CryptoDataService.fetch_crypto_data(symbols)

        if data:
            # 更新数据库
            CryptoDataService.update_database(data)
            logger.info(f"成功更新 {len(data)} 种加密货币的价格")
            return f"成功更新 {len(data)} 种加密货币的价格"
        else:
            logger.warning("未能获取到加密货币数据")
            return "未能获取到加密货币数据"

    except Exception as e:
        # 记录错误并重试
        logger.error(f"更新加密货币价格时出错: {str(e)}")

        # 使用指数退避策略重试任务（10秒, 20秒, 40秒后重试）
        countdown = 2**self.request.retries * 10
        raise self.retry(exc=e, countdown=countdown)
