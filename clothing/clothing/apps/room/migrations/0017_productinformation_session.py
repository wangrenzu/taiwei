# Generated by Django 4.2.2 on 2023-07-05 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("room", "0016_productinformation_live_time"),
    ]

    operations = [
        migrations.AddField(
            model_name="productinformation",
            name="session",
            field=models.CharField(max_length=10, null=True, verbose_name="场次"),
        ),
    ]