# Generated by Django 4.2.2 on 2023-07-19 15:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Script", "0013_collocation_notes"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="script",
            name="type_id",
        ),
    ]
