# Generated by Django 2.1b1 on 2018-08-08 13:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info_data', '0007_auto_20180803_1936'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UsedTransactions',
        ),
        migrations.RemoveField(
            model_name='releasedtradesinfo',
            name='is_profit_fixated',
        ),
        migrations.RemoveField(
            model_name='releasedtradesinfo',
            name='text_to_release_btc',
        ),
    ]