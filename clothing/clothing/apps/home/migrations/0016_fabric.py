# Generated by Django 3.2.9 on 2023-06-25 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_alter_newstyle_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fabric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(blank=True, verbose_name='日期')),
                ('merchant_code', models.CharField(max_length=100, null=True, verbose_name='款号')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='金额')),
                ('channel', models.CharField(blank=True, max_length=100, null=True, verbose_name='渠道')),
                ('role', models.CharField(blank=True, max_length=100, null=True, verbose_name='用途')),
            ],
            options={
                'verbose_name': '面料表',
                'verbose_name_plural': '面料表',
                'db_table': 'taiwei_fabric',
            },
        ),
    ]
