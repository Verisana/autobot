# Generated by Django 2.1b1 on 2018-08-26 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('btcbot', '0015_opentrades_marked_paid'),
    ]

    operations = [
        migrations.AddField(
            model_name='opentrades',
            name='sent_qiwi',
            field=models.BooleanField(default=False),
        ),
    ]
