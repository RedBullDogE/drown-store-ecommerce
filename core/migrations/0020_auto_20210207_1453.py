# Generated by Django 2.2.13 on 2021-02-07 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20210207_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='ref_code',
            field=models.CharField(default='oJPpGjpVul1Q48XRVhjl', max_length=20, unique=True),
        ),
    ]
