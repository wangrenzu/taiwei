# Generated by Django 3.2.9 on 2023-06-25 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0010_alter_onecommodity_date_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='newStyle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200, verbose_name='款号')),
                ('designer', models.CharField(max_length=200, null=True, verbose_name='设计师')),
                ('number_of_pieces', models.CharField(max_length=200, null=True, verbose_name='件数')),
                ('total_number_of_pieces', models.IntegerField(null=True, verbose_name='总件数')),
                ('order_maker', models.CharField(max_length=200, null=True, verbose_name='做下单表人')),
                ('confirmation_on_the_day', models.CharField(max_length=200, null=True, verbose_name='当天确认')),
                ('fabric_arrival_time', models.DateField(null=True, verbose_name='面料到库时间')),
                ('circulation_table_flow_down_time', models.DateField(null=True, verbose_name='流转表流下时间')),
                ('material_fill_craft_package_material_post_road', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='面辅料+充绒+工艺+包材+后道')),
                ('category', models.CharField(max_length=200, null=True, verbose_name='类目')),
            ],
            options={
                'verbose_name': '新款',
                'verbose_name_plural': '新款',
                'db_table': 'taiwei_new_style',
            },
        ),
        migrations.CreateModel(
            name='repeatOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='日期')),
                ('code', models.CharField(max_length=200, verbose_name='款号')),
                ('number_of_pieces', models.CharField(max_length=255, null=True, verbose_name='件数')),
                ('total_number_of_pieces', models.IntegerField(null=True, verbose_name='总件数')),
                ('circulation', models.DateField(null=True, verbose_name='做流转表')),
                ('daily_status', models.CharField(max_length=200, null=True, verbose_name='当日状况')),
                ('fabric_arrival_time', models.DateField(null=True, verbose_name='面料到库时间')),
                ('circulation_table_flow_down', models.DateField(null=True, verbose_name='流转表流下')),
            ],
            options={
                'verbose_name': '翻单',
                'verbose_name_plural': '翻单',
                'db_table': 'taiwei_repeat_orderrrrrrr',
            },
        ),
        migrations.AlterField(
            model_name='onecommodity',
            name='date_time',
            field=models.DateField(verbose_name='日期'),
        ),
    ]
