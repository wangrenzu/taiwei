from django.db import models


# Create your models here.

class Design(models.Model):
    code = models.CharField(verbose_name="款号", max_length=30, null=True)
    name = models.CharField(verbose_name="货品名", max_length=30, null=True)
    designer = models.CharField(verbose_name="设计师", max_length=255, null=True)
    material = models.CharField(verbose_name="季节", max_length=255, null=True)
    specification_quantity = models.CharField(verbose_name="规格数量", max_length=255, null=True)

    class Meta:
        verbose_name = '商品设计'
        verbose_name_plural = '商品设计'
        db_table = 'taiwei_design'


class Tags(models.Model):
    tags = models.CharField(verbose_name="标签", max_length=30)
    design = models.ForeignKey(to=Design, on_delete=models.CASCADE, related_name="tags")
    notes = models.CharField(verbose_name="描述", max_length=255, null=True)

    class Meta:
        verbose_name = '商品设计标签'
        verbose_name_plural = '商品设计标签'
        db_table = 'taiwei_design_tags'


class Size(models.Model):
    size = models.CharField(verbose_name="尺码", max_length=10, default="M")
    weight = models.IntegerField(verbose_name="体重", default=80)
    height = models.IntegerField(verbose_name="身高", default=160)
    tags = models.ForeignKey(to=Tags, on_delete=models.CASCADE, related_name="size")

    class Meta:
        verbose_name = "商品设计尺码"
        verbose_name_plural = '商品设计尺码'
        db_table = 'taiwei_design_size'


class Script(models.Model):
    original = models.CharField(verbose_name="原话语", max_length=1000, null=True)
    gpt_original = models.CharField(verbose_name="gpt加工话语", max_length=1000, null=True)
    tags = models.ForeignKey(to=Tags, on_delete=models.CASCADE, related_name="script")

    class Meta:
        verbose_name = "商品设计话术"
        verbose_name_plural = '商品设计话术'
        db_table = 'taiwei_design_script'


class Collocation(models.Model):
    codes = models.CharField(verbose_name="款号", max_length=255, default="")
    notes = models.CharField(max_length=255, verbose_name="描述", null=True)
    tags = models.ForeignKey(to=Tags, on_delete=models.CASCADE, related_name="collocation")
    child_code = models.CharField(verbose_name="子款号", max_length=255, null=True)

    class Meta:
        verbose_name = "商品搭配"
        verbose_name_plural = '商品搭配'
        db_table = 'taiwei_design_collocation'
