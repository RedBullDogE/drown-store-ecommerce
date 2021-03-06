# Generated by Django 2.2.13 on 2021-02-02 21:12

import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20210202_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='first_name',
            field=models.CharField(default='Drew', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='last_name',
            field=models.CharField(default='Shka', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='address',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+380443567823', max_length=20, region=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='HeVAv2J1BN8Z7AduQPXw', max_length=20, unique=True),
        ),
    ]
