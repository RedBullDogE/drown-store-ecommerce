# Generated by Django 2.2.13 on 2021-02-05 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210202_2112'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='address_type',
        ),
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='rcxdflsFRJs32TsZw29Q', max_length=20, unique=True),
        ),
    ]