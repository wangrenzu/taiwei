# Generated by Django 3.2.9 on 2023-06-25 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_alter_fabric_role'),
    ]

    operations = [
        migrations.CreateModel(
            name='Factory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=100, null=True, verbose_name='款号')),
                ('date', models.DateField(null=True, verbose_name='日期')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='总金额')),
                ('factory', models.CharField(blank=True, max_length=30, null=True, verbose_name='工厂')),
            ],
            options={
                'verbose_name': '工厂表',
                'verbose_name_plural': '工厂表',
                'db_table': 'taiwei_factory',
            },
        ),
    ]
