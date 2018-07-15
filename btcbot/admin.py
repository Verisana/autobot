from django.contrib import admin
from autobot.CustomModelAdminMixin import CustomModelAdminMixin
from .models import BotSetting, AdSetting, MeanBuyTrades


class BotSettingAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    save_on_top = True


class AdSettingAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    save_on_top = True


class MeanBuyTradesAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    save_on_top = True


admin.site.register(BotSetting, BotSettingAdmin)
admin.site.register(AdSetting, AdSettingAdmin)
admin.site.register(MeanBuyTrades, MeanBuyTradesAdmin)