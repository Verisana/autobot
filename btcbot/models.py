from django.db import models


class BotSetting(models.Model):
    name = models.CharField(max_length=64, unique=True)
    api_key = models.ForeignKey('profiles.APIKey',
                                 on_delete=models.CASCADE)
    api_key_qiwi = models.ForeignKey('profiles.APIKeyQiwi',
                                 on_delete=models.CASCADE)
    buy_ad_settings = models.ForeignKey('btcbot.AdSetting',
                                        on_delete=models.CASCADE,
                                        related_name='buy_ad',
                                        )
    sell_ad_settings = models.ForeignKey('btcbot.AdSetting',
                                         on_delete=models.CASCADE,
                                         related_name='sell_ad',
                                         )
    target_profit = models.DecimalField(max_digits=9,
                                        decimal_places=2,
                                    )
    volume_max = models.IntegerField(null=True,
                                    )
    volume_min = models.IntegerField(null=True,
                                     )
    switch = models.BooleanField(default=False)
    greetings_text = models.TextField(blank=True, null=True)
    farewell_text = models.TextField(blank=True, null=True)

    def __str__(self):
        return '%s' % self.name

class AdSetting(models.Model):
    name = models.CharField(max_length=64, unique=True)
    ad_id = models.IntegerField(unique=True)
    trade_direction = models.CharField(max_length=64,
                                       choices=(('buy-bitcoins-online',
                                                 'ONLINE_SELL'),
                                                ('sell-bitcoins-online',
                                                 'ONLINE_BUY')
                                                ))
    payment_method = models.CharField(
                                max_length=64,
                                choices=(('qiwi', 'QIWI'),
                                         ('cash-deposit', 'CASH_DEPOSIT'),
                                         ('transfers-with-specific-bank', 'SPECIFIC_BANK'),
                                         ('yandex-money', 'YANDEXMONEY')))
    def __str__(self):
        return '%s' % self.name


class MeanBuyTrades(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    btc_amount = models.DecimalField(max_digits=10,
                                     decimal_places=8)
    price_rub = models.DecimalField(max_digits=9,
                                    decimal_places=2)
    def __str__(self):
        return 'Buy_active: %d' % self.created_at