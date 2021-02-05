# Generated by Django 2.2.13 on 2021-02-01 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20210201_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='18W2OhUEIf3BcZhmjf36', max_length=20, unique=True),
        ),
    ]