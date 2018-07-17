from django.db import models


class AdInfo(models.Model):
    contragent = models.CharField(max_length=128)
    updated_at = models.DateTimeField()
    trade_type = models.CharField(max_length=32)
    ad_id = models.IntegerField()
    price = models.DecimalField(max_digits=9,
                                decimal_places=2)
    payment_window = models.IntegerField()
    min_amount = models.IntegerField()
    max_amount = models.IntegerField()
    price_usd = models.DecimalField(max_digits=9,
                                    decimal_places=2)
    payment_method = models.CharField(max_length=32)
    username = models.ForeignKey('profiles.Profile',
                                 on_delete=models.CASCADE)
    page_number = models.IntegerField()
    def __str__(self):
        return '%s - %s - %s' % (self.contragent, self.trade_type, self.payment_method)


class ReleasedTradesInfo(models.Model):
    ad_id = models.IntegerField()
    trade_type = models.CharField(max_length=32)
    payment_method = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now=True)
    released_at = models.DateTimeField()
    reference_code = models.CharField(max_length=20)
    contact_id = models.IntegerField()
    amount_rub = models.DecimalField(max_digits=9,
                                     decimal_places=2)
    amount_btc = models.DecimalField(max_digits=10,
                                     decimal_places=8)
    fee_btc = models.DecimalField(max_digits=10,
                                  decimal_places=8)
    rate_rub = models.DecimalField(max_digits=9,
                                   decimal_places=2)
    seller = models.CharField(max_length=128)
    buyer = models.CharField(max_length=128)
    profit_rub = models.DecimalField(max_digits=9,
                                     decimal_places=2,
                                     blank=True,
                                     null=True,
                                    )
    def __str__(self):
        return '%d' % self.ad_id


class TradeReports(models.Model):
    sum_buy_rub = models.DecimalField(max_digits=9,
                                      decimal_places=2,
                                      blank=True,
                                      null=True)
    sum_buy_btc = models.DecimalField(max_digits=10,
                                      decimal_places=8,
                                      blank=True,
                                      null=True,
                                      )
    mean_buy_price = models.DecimalField(max_digits=9,
                                         decimal_places=2,
                                         blank=True,
                                         null=True,
                                         )
    sum_sell_rub = models.DecimalField(max_digits=9,
                                       decimal_places=2,
                                       blank=True,
                                       null=True,
                                       )
    sum_sell_btc = models.DecimalField(max_digits=10,
                                       decimal_places=8,
                                       blank=True,
                                       null=True,
                                       )
    mean_sell_price = models.DecimalField(max_digits=9,
                                          decimal_places=2,
                                          blank=True,
                                          null=True,
                                          )
    num_trades_buy = models.IntegerField(blank=True,
                                         null=True,
                                         )
    num_trades_sell = models.IntegerField(blank=True,
                                          null=True,
                                          )
    profit = models.DecimalField(max_digits=9,
                                 decimal_places=2,
                                 blank=True,
                                 null=True,
                                 )
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'Report %d' % self.created_at