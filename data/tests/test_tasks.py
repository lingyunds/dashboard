from unittest.mock import MagicMock, patch

import pytest
from celery.exceptions import Retry

from data.tasks import update_crypto_prices


class TestCryptoTasks:
    """Celery 任务测试类"""

    @pytest.fixture(autouse=True)
    def setup(self):
        """每个测试前的设置"""
        from data.models import CryptoCurrency

        CryptoCurrency.objects.create(name="Bitcoin", symbol="BTC")
        CryptoCurrency.objects.create(name="Ethereum", symbol="ETH")

    @pytest.mark.django_db
    @patch("data.tasks.CryptoDataService.fetch_crypto_data")
    @patch("data.tasks.CryptoDataService.update_database")
    @patch("data.tasks.logger")
    def test_update_crypto_prices_success(self, mock_logger, mock_update, mock_fetch):
        """测试任务成功执行的情况"""
        # 模拟 API 返回数据
        mock_fetch.return_value = {"bitcoin": {"usd": 45000.50}, "ethereum": {"usd": 3000.75}}

        # 调用任务
        result = update_crypto_prices()

        # 断言
        mock_fetch.assert_called_once()
        mock_update.assert_called_once()
        mock_logger.info.assert_called()
        assert "成功更新" in result
        assert "2" in result  # 2种加密货币

    @pytest.mark.django_db
    @patch("data.tasks.CryptoDataService.fetch_crypto_data")
    @patch("data.tasks.CryptoDataService.update_database")
    @patch("data.tasks.logger")
    def test_update_crypto_prices_no_data(self, mock_logger, mock_update, mock_fetch):
        """测试没有获取到数据的情况"""
        mock_fetch.return_value = None

        result = update_crypto_prices()

        mock_fetch.assert_called_once()
        mock_update.assert_not_called()
        mock_logger.warning.assert_called_with("未能获取到加密货币数据")
        assert result == "未能获取到加密货币数据"

    @pytest.mark.django_db
    @patch("data.tasks.CryptoDataService.fetch_crypto_data")
    @patch("data.tasks.logger")
    def test_update_crypto_prices_retry_on_exception(self, mock_logger, mock_fetch):
        """测试异常情况下的重试逻辑"""
        mock_fetch.side_effect = Exception("API Error")

        # 模拟 self.retry
        with patch.object(update_crypto_prices, "retry") as mock_retry:
            mock_retry.side_effect = Retry()

            # 调用任务，应该抛出 Retry 异常
            with pytest.raises(Retry):
                update_crypto_prices()

            # 断言重试被调用
            mock_retry.assert_called_once()
            mock_logger.error.assert_called()
