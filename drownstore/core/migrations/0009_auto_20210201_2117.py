# Generated by Django 2.2.13 on 2021-02-01 21:17

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20210201_2104'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='time_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='tArFJuaGmhGl74zgPk1L', max_length=20, unique=True),
        ),
    ]
