# Generated by Django 2.1b1 on 2018-07-25 08:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0013_auto_20180724_2334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apikeyqiwi',
            name='order',
        ),
    ]
