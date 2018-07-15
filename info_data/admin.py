from django.contrib import admin
from autobot.CustomModelAdminMixin import CustomModelAdminMixin
from .models import AdInfo, ReleasedTradesInfo, TradeReports


class AdInfoAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    list_filter = ['min_amount',
                   'max_amount',
                   'page_number',
                   'trade_type',
                   'payment_method',]
    save_on_top = True


class ReleasedTradesInfoAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    list_filter = ['trade_type',
                   'payment_method']
    date_hierarchy = 'released_at'
    save_on_top = True


class TradeReportsAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    save_on_top = True


admin.site.register(AdInfo, AdInfoAdmin)
admin.site.register(ReleasedTradesInfo, ReleasedTradesInfoAdmin)
admin.site.register(TradeReports, TradeReportsAdmin)