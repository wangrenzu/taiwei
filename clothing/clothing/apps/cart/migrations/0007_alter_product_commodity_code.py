# Generated by Django 3.2.9 on 2023-06-02 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0006_alter_product_commodity_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='commodity_code',
            field=models.CharField(blank=True, max_length=255, null=True, unique=True, verbose_name='款号'),
        ),
    ]