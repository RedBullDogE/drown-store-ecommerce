# Generated by Django 2.2.13 on 2021-02-07 15:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20210207_1453'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='discount_type',
            field=models.CharField(choices=[('A', 'Absolute'), ('R', 'Relative')], default='A', max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='A2eWx3tPxGiR7nBDNXNr', max_length=20, unique=True),
        ),
    ]