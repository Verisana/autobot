# Generated by Django 2.1b1 on 2018-08-01 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('info_data', '0004_usedtransactions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='releasedtradesinfo',
            name='released_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
