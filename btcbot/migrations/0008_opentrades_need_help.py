# Generated by Django 2.1b1 on 2018-07-29 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('btcbot', '0007_remove_opentrades_left_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='opentrades',
            name='need_help',
            field=models.BooleanField(default=False),
        ),
    ]
