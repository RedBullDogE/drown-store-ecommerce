# Generated by Django 2.2.13 on 2021-02-02 16:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20210202_1241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='billing_address',
        ),
        migrations.AlterField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Payment'),
        ),
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='3tQsud4x2xtsU5AB5fdv', max_length=20, unique=True),
        ),
    ]