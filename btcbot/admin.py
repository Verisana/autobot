from django.contrib import admin
from autobot.CustomModelAdminMixin import CustomModelAdminMixin
from .models import BotSetting, AdSetting, MeanBuyTrades


class BotSettingAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ['name',
              'switch_buy_ad_upd',
              'switch_sell_ad_upd',
              'switch_bot_buy',
              'switch_bot_sell',
              'switch_bot_send_rev',
              'target_profit',
              'volume_min',
              'volume_max',
              'greetings_text',
              'farewell_text',
              'review_text',
              'buy_ad_settings',
              'sell_ad_settings',
              'api_key_qiwi',
             ]
    list_display = ['name',
                    'switch_buy_ad_upd',
                    'switch_sell_ad_upd',
                    'switch_bot_buy',
                    'switch_bot_sell',
                    'switch_bot_send_rev',
                    'target_profit',
                    'volume_min',
                    'volume_max',
                    'buy_ad_settings',
                    'sell_ad_settings',
                ]
    filter_horizontal = ['api_key_qiwi']


class AdSettingAdmin(admin.ModelAdmin):
    # Include all fields except id and my_price
    fields = [field.name for field in AdSetting._meta.fields if field.name != 'id']
    list_display = [field.name for field in AdSetting._meta.fields if field.name != 'id']
    save_on_top = True


class MeanBuyTradesAdmin(CustomModelAdminMixin, admin.ModelAdmin):
    save_on_top = True


admin.site.register(BotSetting, BotSettingAdmin)
admin.site.register(AdSetting, AdSettingAdmin)
admin.site.register(MeanBuyTrades, MeanBuyTradesAdmin)