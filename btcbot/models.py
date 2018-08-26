from django.db import models


class BotSetting(models.Model):
    name = models.CharField(max_length=64, unique=True)
    api_key_qiwi = models.ManyToManyField('profiles.APIKeyQiwi', blank=True)
    buy_ad_settings = models.ForeignKey('btcbot.AdSetting',
                                        on_delete=models.CASCADE,
                                        related_name='buy_ad')
    sell_ad_settings = models.ForeignKey('btcbot.AdSetting',
                                         on_delete=models.CASCADE,
                                         related_name='sell_ad')
    telegram_bot_settings = models.ForeignKey('profiles.TelegramBotSettings', on_delete=models.CASCADE,
                                               blank=True,
                                               null=True)
    target_profit = models.IntegerField()
    qiwi_profit_fee = models.DecimalField(max_digits=2, decimal_places=1, default='1.8')
    volume_max = models.IntegerField(null=True)
    volume_min = models.IntegerField(null=True)
    switch_buy_ad_upd = models.BooleanField(default=False)
    switch_sell_ad_upd = models.BooleanField(default=False)
    switch_bot_buy = models.BooleanField(default=False)
    switch_bot_sell = models.BooleanField(default=False)
    switch_rev_send_sell = models.BooleanField(default=False)
    switch_rev_send_buy = models.BooleanField(default=False)
    switch_profit_fixator = models.BooleanField(default=True)
    all_wallets_blocked = models.BooleanField(default=False)
    is_ad_visible = models.BooleanField(default=False)
    qiwi_limit = models.IntegerField(default=50000)
    greetings_text = models.TextField(blank=True, null=True)
    farewell_text = models.TextField(blank=True, null=True)
    review_text = models.TextField(blank=True, null=True)

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
    my_price = models.IntegerField(null=True, blank=True)
    stop_price = models.DecimalField(max_digits=9,
                                     decimal_places=2,
                                     blank=True,
                                     null=True)
    api_key = models.ForeignKey('profiles.APIKey',
                                on_delete=models.CASCADE)
    def __str__(self):
        return '%s' % self.name


class MeanBuyTrades(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    btc_amount = models.DecimalField(max_digits=10, decimal_places=8, null=True)
    price_rub = models.DecimalField(max_digits=9, decimal_places=2)
    is_fee_accounted = models.BooleanField(default=False)
    def __str__(self):
        return 'Buy_active: %s' % str(self.created_at)

class OpenTrades(models.Model):
    trade_id = models.IntegerField()
    contragent = models.CharField(max_length=128)
    is_verified = models.BooleanField(default=False)
    amount_rub = models.DecimalField(max_digits=9,
                                     decimal_places=2)
    amount_btc = models.DecimalField(max_digits=10,
                                     decimal_places=8)
    created_at = models.DateTimeField(auto_now=True)
    reference_text = models.CharField(max_length=256)
    api_key_qiwi = models.ForeignKey('profiles.APIKeyQiwi', on_delete=models.CASCADE, blank=True, null=True)
    sent_first_message = models.BooleanField(default=False)
    sent_qiwi = models.BooleanField(default=False)
    marked_paid = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    who_marked_paid = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, blank=True, null=True)
    sent_second_message = models.BooleanField(default=False)
    disputed = models.BooleanField(default=False)
    def __str__(self):
        return 'Open trade #%d' % self.trade_id