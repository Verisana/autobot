# Generated by Django 2.1b1 on 2018-08-08 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('btcbot', '0011_meanbuytrades_is_fee_accounted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='opentrades',
            name='need_help',
        ),
    ]