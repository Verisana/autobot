from django.contrib import admin
from autobot.CustomModelAdminMixin import CustomModelAdminMixin
from .models import BotSetting, AdSetting, MeanBuyTrades, OpenTrades


class BotSettingAdmin(admin.ModelAdmin):
    save_on_top = True
    fields = ['name',
              'switch_buy_ad_upd',
              'switch_sell_ad_upd',
              'switch_bot_buy',
              'switch_bot_sell',
              'switch_rev_send_sell',
              'switch_rev_send_buy',
              'target_profit',
              'volume_min',
              'volume_max',
              'greetings_text',
              'farewell_text',
              'review_text',
              'buy_ad_settings',
              'sell_ad_settings',
              'api_key_qiwi',
              'telegram_bot_settings'
             ]
    list_display = ['name',
                    'switch_buy_ad_upd',
                    'switch_sell_ad_upd',
                    'switch_bot_buy',
                    'switch_bot_sell',
                    'switch_rev_send_sell',
                    'switch_rev_send_buy',
                    'target_profit',
                    'volume_min',
                    'volume_max',
                    'buy_ad_settings',
                    'sell_ad_settings',
                    'telegram_bot_settings',
                    ]
    filter_horizontal = ['api_key_qiwi']


class AdSettingAdmin(admin.ModelAdmin):
    # Include all fields except id and my_price
    fields = [field.name for field in AdSetting._meta.fields if field.name != 'id' and field.name != 'stop_price']
    list_display = [field.name for field in AdSetting._meta.fields if field.name != 'id']
    save_on_top = True


class MeanBuyTradesAdmin(admin.ModelAdmin):
    fields = [field.name for field in MeanBuyTrades._meta.fields if field.name != 'id' and field.name != 'created_at']
    list_display = [field.name for field in MeanBuyTrades._meta.fields if field.name != 'id']
    save_on_top = True

class OpenTradesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in OpenTrades._meta.fields if field.name != 'id']
    save_on_top = True


admin.site.register(BotSetting, BotSettingAdmin)
admin.site.register(AdSetting, AdSettingAdmin)
admin.site.register(MeanBuyTrades, MeanBuyTradesAdmin)
admin.site.register(OpenTrades, OpenTradesAdmin)