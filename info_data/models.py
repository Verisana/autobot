from django.db import models


class ReleasedTradesInfo(models.Model):
    ad_id = models.IntegerField()
    trade_type = models.CharField(max_length=32)
    payment_method = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now=True)
    released_at = models.DateTimeField(null=True, blank=True)
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
    is_qiwi_blocked = models.BooleanField(default=False)
    disputed=models.BooleanField(default=False)
    who_released_btc = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE, blank=True, null=True)
    deal_processed_time = models.DurationField(blank=True, null=True)
    def __str__(self):
        return '%d' % self.ad_id

class OperatorsWorkingShift(models.Model):
    start_working = models.DateTimeField()
    operator = models.ForeignKey('profiles.Profile', on_delete=models.CASCADE)
    end_working = models.DateTimeField(blank=True, null=True)
    shift_duration = models.DurationField(blank=True, null=True)
    number_of_deals = models.IntegerField(blank=True, null=True)
    mean_deal_processing = models.DurationField(blank=True, null=True)
    amount_sell_rub = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    amount_sell_btc = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    profit_rub = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '%s' % self.operator