# Generated by Django 3.2.9 on 2023-06-25 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0016_fabric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabric',
            name='time',
            field=models.DateField(blank=True, verbose_name='日期'),
        ),
    ]
