# Generated by Django 2.1b1 on 2018-07-19 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('btcbot', '0007_auto_20180719_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='adsetting',
            name='stop_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
    ]