# Generated by Django 4.2.2 on 2023-06-30 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0027_stylestatus_is_other"),
    ]

    operations = [
        migrations.AddField(
            model_name="stylestatus",
            name="num",
            field=models.IntegerField(null=True, verbose_name="来几次"),
        ),
    ]