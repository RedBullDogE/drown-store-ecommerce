# Generated by Django 2.2.13 on 2021-02-06 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20210205_2129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='49D9qnAq85iPODf1XApN', max_length=20, unique=True),
        ),
    ]
