# Generated by Django 2.2.13 on 2021-02-16 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20210215_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='pM3mbtO1yMtDSAdKgsjE', max_length=20, unique=True),
        ),
    ]