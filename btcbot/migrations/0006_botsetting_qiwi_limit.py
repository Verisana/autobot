# Generated by Django 2.1b1 on 2018-07-25 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('btcbot', '0005_auto_20180725_1557'),
    ]

    operations = [
        migrations.AddField(
            model_name='botsetting',
            name='qiwi_limit',
            field=models.IntegerField(default=50000),
        ),
    ]
