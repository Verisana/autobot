# Generated by Django 2.1b1 on 2018-08-15 17:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('btcbot', '0012_remove_opentrades_need_help'),
    ]

    operations = [
        migrations.AddField(
            model_name='opentrades',
            name='who_marked_paid',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
