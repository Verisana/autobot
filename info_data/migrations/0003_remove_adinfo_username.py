# Generated by Django 2.1b1 on 2018-07-18 17:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info_data', '0002_adinfo_order_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adinfo',
            name='username',
        ),
    ]
