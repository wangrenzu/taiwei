# Generated by Django 3.2.9 on 2023-06-06 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_updatestatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='updatestatus',
            name='name',
            field=models.CharField(max_length=30, unique=True, verbose_name='名称'),
        ),
    ]