# Generated by Django 2.2.13 on 2021-02-07 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20210207_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='RY51Cf5yh71IWG675Adh', max_length=20, unique=True),
        ),
    ]
