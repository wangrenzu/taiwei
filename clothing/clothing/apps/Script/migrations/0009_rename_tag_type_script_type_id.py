# Generated by Django 4.2.2 on 2023-07-17 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Script", "0008_script"),
    ]

    operations = [
        migrations.RenameField(
            model_name="script",
            old_name="tag_type",
            new_name="type_id",
        ),
    ]
