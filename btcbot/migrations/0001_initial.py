# Generated by Django 2.1b1 on 2018-07-25 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('ad_id', models.IntegerField(unique=True)),
                ('trade_direction', models.CharField(choices=[('buy-bitcoins-online', 'ONLINE_SELL'), ('sell-bitcoins-online', 'ONLINE_BUY')], max_length=64)),
                ('payment_method', models.CharField(choices=[('qiwi', 'QIWI'), ('cash-deposit', 'CASH_DEPOSIT'), ('transfers-with-specific-bank', 'SPECIFIC_BANK'), ('yandex-money', 'YANDEXMONEY')], max_length=64)),
                ('my_price', models.IntegerField(blank=True, null=True)),
                ('stop_price', models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BotSetting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('target_profit', models.IntegerField()),
                ('qiwi_profit_fee', models.DecimalField(decimal_places=1, default='1.8', max_digits=2)),
                ('volume_max', models.IntegerField(null=True)),
                ('volume_min', models.IntegerField(null=True)),
                ('switch_buy_ad_upd', models.BooleanField(default=False)),
                ('switch_sell_ad_upd', models.BooleanField(default=False)),
                ('switch_bot_buy', models.BooleanField(default=False)),
                ('switch_bot_sell', models.BooleanField(default=False)),
                ('switch_rev_send_sell', models.BooleanField(default=False)),
                ('switch_rev_send_buy', models.BooleanField(default=False)),
                ('switch_profit_fixator', models.BooleanField(default=True)),
                ('is_ad_visible', models.BooleanField(default=False)),
                ('greetings_text', models.TextField(blank=True, null=True)),
                ('farewell_text', models.TextField(blank=True, null=True)),
                ('review_text', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='MeanBuyTrades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('btc_amount', models.DecimalField(decimal_places=8, max_digits=10, null=True)),
                ('price_rub', models.DecimalField(decimal_places=2, max_digits=9)),
            ],
        ),
        migrations.CreateModel(
            name='OpenTrades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_id', models.IntegerField()),
                ('contragent', models.CharField(max_length=128)),
                ('amount_rub', models.DecimalField(decimal_places=2, max_digits=9)),
                ('amount_btc', models.DecimalField(decimal_places=8, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('reference_text', models.CharField(max_length=256)),
                ('sent_first_message', models.BooleanField(default=False)),
                ('paid', models.BooleanField(default=False)),
                ('sent_second_message', models.BooleanField(default=False)),
                ('left_review', models.BooleanField(default=False)),
                ('disputed', models.BooleanField(default=False)),
            ],
        ),
    ]
