from django.db import models


# Create your models here.
class DouyinUser(models.Model):
    douyin_id = models.CharField(max_length=255, verbose_name="抖音ID")
    is_fan_group = models.SmallIntegerField(default=0, verbose_name="是否是粉丝团")
    style_number = models.CharField(max_length=255, verbose_name="款号")
    time = models.IntegerField(verbose_name="时间")
    date = models.DateField(verbose_name="日期", auto_now=True)
    username = models.CharField(max_length=255, verbose_name="用户名")

    class Meta:
        verbose_name = "抖音用户"
        verbose_name_plural = "抖音用户们"
        db_table = "taiwei_douyin_user"
