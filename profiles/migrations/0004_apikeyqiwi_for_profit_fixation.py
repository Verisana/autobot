# Generated by Django 2.1b1 on 2018-07-26 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_remove_apikeyqiwi_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='apikeyqiwi',
            name='for_profit_fixation',
            field=models.BooleanField(default=False),
        ),
    ]
