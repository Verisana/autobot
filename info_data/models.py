from django.db import models


class ReleasedTradesInfo(models.Model):
    ad_id = models.IntegerField()
    trade_type = models.CharField(max_length=32)
    payment_method = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now=True)
    released_at = models.DateTimeField()
    reference_code = models.CharField(max_length=20)
    contact_id = models.IntegerField()
    amount_rub = models.DecimalField(max_digits=9, decimal_places=2)
    amount_btc = models.DecimalField(max_digits=10, decimal_places=8)
    fee_btc = models.DecimalField(max_digits=10, decimal_places=8)
    rate_rub = models.DecimalField(max_digits=9, decimal_places=2)
    seller = models.CharField(max_length=128)
    buyer = models.CharField(max_length=128)
    profit_rub_trade = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    profit_rub_full = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    api_key_qiwi = models.ForeignKey('profiles.APIKeyQiwi', on_delete=models.CASCADE)
    def __str__(self):
        return '%d' % self.ad_id