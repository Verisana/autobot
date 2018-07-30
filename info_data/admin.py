from django.contrib import admin
from .models import ReleasedTradesInfo, UsedTransactions


class ReleasedTradesInfoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ReleasedTradesInfo._meta.fields if field.name != 'id']
    list_filter = ['trade_type',
                   'payment_method']
    date_hierarchy = 'released_at'
    save_on_top = True


class UsedTransactionsAdmin(admin.ModelAdmin):
    list_display = [field.name for field in UsedTransactions._meta.fields if field.name != 'id']
    save_on_top = True
    date_hierarchy = 'created_at'


admin.site.register(ReleasedTradesInfo, ReleasedTradesInfoAdmin)
admin.site.register(UsedTransactions, UsedTransactionsAdmin)