# Generated by Django 3.2.9 on 2023-06-17 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onecommodity',
            name='date_time',
            field=models.DateField(),
        ),
    ]