# Generated by Django 2.1b1 on 2018-07-24 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('btcbot', '0016_botsetting_qiwi_profit_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='botsetting',
            name='switch_profit_fixator',
            field=models.BooleanField(default=True),
        ),
    ]
