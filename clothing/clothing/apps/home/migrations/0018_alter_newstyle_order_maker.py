# Generated by Django 3.2.9 on 2023-06-25 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0017_alter_fabric_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newstyle',
            name='order_maker',
            field=models.DateField(max_length=200, null=True, verbose_name='做下单表'),
        ),
    ]
