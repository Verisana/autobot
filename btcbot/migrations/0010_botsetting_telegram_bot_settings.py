# Generated by Django 2.1b1 on 2018-07-22 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0010_auto_20180722_2355'),
        ('btcbot', '0009_auto_20180721_0054'),
    ]

    operations = [
        migrations.AddField(
            model_name='botsetting',
            name='telegram_bot_settings',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.TelegramBotSettings'),
        ),
    ]
