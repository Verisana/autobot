# Generated by Django 2.1b1 on 2018-08-03 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info_data', '0006_auto_20180803_0055'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='releasedtradesinfo',
            name='reference_code',
        ),
        migrations.AddField(
            model_name='releasedtradesinfo',
            name='text_to_release_btc',
            field=models.TextField(blank=True, null=True),
        ),
    ]
