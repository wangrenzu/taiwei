from django.apps import AppConfig


class HomeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'home'
    verbose_name = "信息管理"
    verbose_name_plural = verbose_name
