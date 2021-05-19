from django.contrib import admin
from .models import ReleasedTradesInfo, OperatorsWorkingShift


class ReleasedTradesInfoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ReleasedTradesInfo._meta.fields if field.name != 'id']
    list_filter = ['trade_type',
                   'payment_method']
    date_hierarchy = 'released_at'
    save_on_top = True


class OperatorsWorkingShiftAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OperatorsWorkingShift._meta.fields if field.name != 'id']
    save_on_top = True


admin.site.register(ReleasedTradesInfo, ReleasedTradesInfoAdmin)
admin.site.register(OperatorsWorkingShift, OperatorsWorkingShiftAdmin)