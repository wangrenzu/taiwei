# Generated by Django 3.2.9 on 2023-06-25 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_alter_newstyle_order_maker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fabric',
            name='role',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='用途'),
        ),
    ]
