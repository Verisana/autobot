# Generated by Django 2.1b1 on 2018-07-30 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('btcbot', '0008_opentrades_need_help'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botsetting',
            name='switch_qiwi_updater',
        ),
    ]
