import os
from celery import Celery
from django.conf import settings

# 设置默认的 Django 设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clothing.settings')

# 创建 Celery 应用
app = Celery('clothing')

# 使用 Django 设置模块来配置 Celery
app.config_from_object(settings, namespace='CELERY')

# 自动发现和注册异步任务
app.autodiscover_tasks()
