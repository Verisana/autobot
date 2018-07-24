# Generated by Django 2.1b1 on 2018-07-23 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info_data', '0005_releasedtradesinfo_api_key_qiwi'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='releasedtradesinfo',
            name='profit_rub',
        ),
        migrations.AddField(
            model_name='releasedtradesinfo',
            name='profit_rub_full',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='releasedtradesinfo',
            name='profit_rub_trade',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
    ]
