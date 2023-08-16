# Generated by Django 4.2.2 on 2023-08-16 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0041_newstylestatustracking_notes_info"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stylestatus",
            name="is_other",
        ),
        migrations.RemoveField(
            model_name="stylestatus",
            name="num",
        ),
        migrations.RemoveField(
            model_name="stylestatus",
            name="remarks",
        ),
        migrations.RemoveField(
            model_name="stylestatus",
            name="tags",
        ),
        migrations.RemoveField(
            model_name="stylestatus",
            name="time",
        ),
        migrations.RemoveField(
            model_name="stylestatus",
            name="time_num",
        ),
        migrations.AddField(
            model_name="stylestatus",
            name="back_rate",
            field=models.FloatField(null=True, verbose_name="退货损耗"),
        ),
        migrations.AddField(
            model_name="stylestatus",
            name="repeat_count",
            field=models.IntegerField(null=True, verbose_name="翻单次数"),
        ),
        migrations.AlterField(
            model_name="stylestatus",
            name="date_time",
            field=models.DateField(null=True, verbose_name="新款下单日期"),
        ),
    ]