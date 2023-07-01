# Generated by Django 3.2.9 on 2023-06-14 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_stock_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, verbose_name='款号')),
                ('size', models.CharField(max_length=200, verbose_name='尺寸')),
            ],
            options={
                'verbose_name': '尺寸',
                'verbose_name_plural': '尺寸',
                'db_table': 'taiwei_size',
            },
        ),
    ]