# Generated by Django 2.2.13 on 2021-02-01 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20210201_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='1mumlhe7eCdetnn1NEEa', max_length=20, unique=True),
        ),
    ]
