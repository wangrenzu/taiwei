# Generated by Django 4.2.2 on 2023-07-14 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0039_goods_describe"),
    ]

    operations = [
        migrations.RenameField(
            model_name="goods",
            old_name="describe",
            new_name="code_describe",
        ),
    ]
