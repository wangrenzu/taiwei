# Generated by Django 4.2.2 on 2023-08-10 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Script", "0022_remove_tags_notes"),
    ]

    operations = [
        migrations.AddField(
            model_name="tags",
            name="notes",
            field=models.CharField(
                default="", max_length=255, null=True, verbose_name="描述"
            ),
        ),
    ]
