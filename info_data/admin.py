from django.contrib import admin
from autobot.CustomModelAdminMixin import CustomModelAdminMixin
from .models import ReleasedTradesInfo, TradeReports


class ReleasedTradesInfoAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    list_filter = ['trade_type',
                   'payment_method']
    date_hierarchy = 'released_at'
    save_on_top = True


class TradeReportsAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    save_on_top = True


admin.site.register(ReleasedTradesInfo, ReleasedTradesInfoAdmin)
admin.site.register(TradeReports, TradeReportsAdmin)