# Generated by Django 2.1b1 on 2018-07-25 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_auto_20180725_1359'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apikeyqiwi',
            name='username',
        ),
    ]
