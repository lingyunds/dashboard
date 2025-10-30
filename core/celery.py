import os

import django
from celery import Celery
from django.conf import settings

# 设置默认的Django设置模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()


app = Celery("core")

# 使用Django的设置文件配置Celery,使用字符串命名空间意味着 Celery 配置不需要在 Windows 上序列化对象
app.config_from_object("django.conf:settings", namespace="CELERY")

# 从所有已注册的Django应用中发现任务（tasks.py）
app.autodiscover_tasks()

# 当被调用时，它会打印出当前任务请求的详细信息，并且不会存储任务的结果。


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
