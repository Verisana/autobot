from decimal import *
from django.utils import timezone
from btcbot.models import BotSetting, OpenTrades
from btcbot.trader.local_api import LocalBitcoin
import telegram

class LocalSellerBot():
    reference_text = 'Сделка на сайте LocalBitcoins.net #'

    def __init__(self, setting_id):
        self.bot = BotSetting.objects.get(id=setting_id)
        self.lbtc = LocalBitcoin(self.bot.sell_ad_settings.api_key.api_key,
                                 self.bot.sell_ad_settings.api_key.api_secret)
        self.qiwi_list = self.bot.api_key_qiwi.filter(is_blocked=False).order_by('used_at')
        self.telegram_bot = telegram.Bot(token=self.bot.telegram_bot_settings.token)
        self.my_ad_info = None
        self.opened_trades = None
        self.all_notifications = None
        if self.bot.is_ad_visible != self.bot.switch_bot_sell:
            self._check_visibility()

    def _get_my_ad_info(self):
        self.my_ad_info = self.lbtc.get_ad_info(self.bot.sell_ad_settings.ad_id).json()

    def _get_opened_trades(self):
        self.opened_trades = self.lbtc.get_dashboard().json()

    def _get_all_notifications(self):
        self.all_notifications = self.lbtc.get_all_notifications().json()

    def _get_appropriate_qiwi(self, deal_price):
        if self.qiwi_list:
            for qiwi in self.qiwi_list:
                balance = qiwi.limit_left - Decimal(deal_price)
                if balance > 0:
                    return qiwi
            message = 'Дневные лимиты по киви кошелькам сожжены. Продажа остановлена.'
            self.telegram_bot.send_message(self.bot.telegram_bot_settings.chat_emerg, message)
            self.bot.switch_bot_sell = False
            self.save(update_fields=['switch_bot_sell'])
            return self.qiwi_list.order_by('-limit_left')[0]
        else:
            message = 'Все киви кошельки заблокированы. Продажа остановлена.'
            self.telegram_bot.send_message(self.bot.telegram_bot_settings.chat_emerg, message)
            self.bot.switch_bot_sell = False
            self.save(update_fields=['switch_bot_sell'])

    def _check_visibility(self):
        if not self.my_ad_info:
            self._get_my_ad_info()
        self.bot.is_ad_visible = self.bot.switch_bot_sell
        self.bot.save(update_fields=['is_ad_visible'])
        if bool(self.my_ad_info['data']['ad_list'][0]['data']['visible']) == self.bot.switch_bot_sell:
            pass
        else:
            self._ad_visible_edit(self.bot.switch_bot_sell)

    def _ad_visible_edit(self, visible):
        if not self.my_ad_info:
            self._get_my_ad_info()
        params = {'price_equation': self.my_ad_info['data']['ad_list'][0]['data']['price_equation'],
                  'lat': self.my_ad_info['data']['ad_list'][0]['data']['lat'],
                  'lon': self.my_ad_info['data']['ad_list'][0]['data']['lon'],
                  'city': self.my_ad_info['data']['ad_list'][0]['data']['city'],
                  'location_string': self.my_ad_info['data']['ad_list'][0]['data']['location_string'],
                  'countrycode': self.my_ad_info['data']['ad_list'][0]['data']['countrycode'],
                  'currency': self.my_ad_info['data']['ad_list'][0]['data']['currency'],
                  'account_info': '',
                  'bank_name': self.my_ad_info['data']['ad_list'][0]['data']['bank_name'],
                  'msg': self.my_ad_info['data']['ad_list'][0]['data']['msg'],
                  'sms_verification_required': self.my_ad_info['data']['ad_list'][0]['data']['sms_verification_required'],
                  'track_max_amount': self.my_ad_info['data']['ad_list'][0]['data']['track_max_amount'],
                  'require_trusted_by_advertiser': self.my_ad_info['data']['ad_list'][0]['data']['require_trusted_by_advertiser'],
                  'require_identification': self.my_ad_info['data']['ad_list'][0]['data']['require_identification'],
                  'min_amount': self.my_ad_info['data']['ad_list'][0]['data']['min_amount'],
                  'max_amount': self.my_ad_info['data']['ad_list'][0]['data']['max_amount'],
                  'details-phone_number': '+0000000000',
                  'visible': visible}
        return self.lbtc.ad_edit(self.bot.sell_ad_settings.ad_id, params)

    def _send_message(self, message, contact_id):
        response = self.lbtc.post_message_to_contact(str(contact_id), message)
        if response.status_code != 200:
            return True
        else:
            return False

    def _is_trade_processed(self, con_id):
        for i in OpenTrades.objects.all():
            if con_id == i.trade_id:
                return True
        return False

    def check_new_trades(self):
        if not self.opened_trades:
            self._get_opened_trades()
        if not self._get_all_notifications():
            self._get_all_notifications()

        for i in self.opened_trades['data']['contact_list']:
            contact_id = i['data']['contact_id']
            ad_id = i['data']['advertisement']['id']
            if not i['data']['disputed_at'] and not self._is_trade_processed(contact_id) and ad_id == self.my_ad_info.ad_id:
                qiwi = self._get_appropriate_qiwi(i['data']['amount'])
                reference_text = self.reference_text + i['data']['reference_code']
                message = self.bot.greetings_text.format(qiwi.phone_number, reference_text)
                new_trade = OpenTrades.objects.create(trade_id=contact_id,
                                                      contragent=i['data']['buyer']['username'],
                                                      amount_rub=i['data']['amount'],
                                                      amount_btc=i['data']['amount_btc'],
                                                      created_at=timezone.now(),
                                                      reference_text=reference_text)
                if self._send_message(message, contact_id):
                    new_trade.sent_first_message = True
                    new_trade.save(update_fields=['sent_first_message'])

                for notification in self.all_notifications['data']:
                    if notification['contact_id'] == contact_id:
                        self.lbtc.mark_notification_as_read(str(notification['id']))
                        break

    def check_payment(self):
        pass