# Generated by Django 4.2.2 on 2023-07-17 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Script", "0005_rename_design_id_tags_design"),
    ]

    operations = [
        migrations.CreateModel(
            name="Size",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "size",
                    models.CharField(default="M", max_length=10, verbose_name="尺码"),
                ),
                ("weight", models.IntegerField(default=80, verbose_name="体重")),
                ("height", models.IntegerField(default=160, verbose_name="身高")),
            ],
            options={
                "verbose_name": "商品设计尺码",
                "verbose_name_plural": "商品设计尺码",
                "db_table": "taiwei_design_size",
            },
        ),
    ]
