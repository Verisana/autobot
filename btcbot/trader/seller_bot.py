from decimal import *
from django.utils import timezone
from btcbot.trader.local_api import LocalBitcoin
from btcbot.trader.ad_bot import AdUpdateBot
from btcbot.qiwi_api import pyqiwi
from btcbot.models import BotSetting, OpenTrades, MeanBuyTrades
from info_data.models import ReleasedTradesInfo
import telegram


class LocalSellerBot():
    reference_text = 'Сделка на сайте LocalBitcoins.net #'

    def __init__(self, setting_id, proxy=None):
        self.bot = BotSetting.objects.get(id=setting_id)
        self.ad_upd = AdUpdateBot(setting_id, proxy=None)
        self.lbtc = LocalBitcoin(self.bot.sell_ad_settings.api_key.api_key,
                                 self.bot.sell_ad_settings.api_key.api_secret,
                                 proxy=proxy)
        self.qiwi_list = self.bot.api_key_qiwi.filter(is_blocked=False).order_by('used_at')
        self.telegram_bot = telegram.Bot(token=self.bot.telegram_bot_settings.token)
        self.my_ad_info = self.bot.sell_ad_settings
        self.opened_trades = None
        self.all_notifications = None
        if self.bot.switch_bot_sell:
            self.bot.switch_sell_ad_upd = True
            self.bot.save(update_fields=['switch_sell_ad_upd'])
        if self.bot.is_ad_visible != self.bot.switch_bot_sell:
            self._check_visibility()

    def _get_my_ad_info(self):
        self.my_ad_info = self.lbtc.get_ad_info(self.bot.sell_ad_settings.ad_id).json()

    def _get_opened_trades(self):
        self.opened_trades = self.lbtc.get_dashboard().json()

    def _get_specific_trade(self, trade_id):
        response = self.lbtc.get_contact_info(str(trade_id))
        if response.status_code == 200:
            return response.json()
        else:
            return response

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
            self.bot.save(update_fields=['switch_bot_sell'])
            return self.qiwi_list.order_by('-limit_left')[0]
        else:
            message = 'Все киви кошельки заблокированы. Продажа остановлена.'
            self.telegram_bot.send_message(self.bot.telegram_bot_settings.chat_emerg, message)
            self.bot.switch_bot_sell = False
            self.bot.save(update_fields=['switch_bot_sell'])

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
        btc_left_to_sell = Decimal('0')
        for i in MeanBuyTrades.objects.all():
            btc_left_to_sell += i.btc_amount
        max_amount = self.bot.sell_ad_settings.stop_price * btc_left_to_sell
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
                  'max_amount': str(round(max_amount, 0)),
                  'details-phone_number': '+0000000000',
                  'visible': visible}
        return self.lbtc.ad_edit(self.bot.sell_ad_settings.ad_id, params)

    def _reduce_buy_leftover(self, sold_btc):
        mbt = MeanBuyTrades.objects.all().order_by('created_at')
        for trade in mbt:
            difference = trade.btc_amount - sold_btc
            if difference > 0:
                trade.btc_amount = difference
                trade.save(update_fields='btc_amount')
                return None
            elif difference == 0:
                trade.delete()
                return None
            else:
                sold_btc -= trade.btc_amount
                if len(mbt) != 1:
                    trade.delete()
                else:
                    trade.btc_amount = 0
                    trade.save(update_fields=['btc_amount'])

        if self.bot.switch_bot_sell:
            message = 'Все битки проданы. Продажа остановлена.'
            self.telegram_bot.send_message(self.bot.telegram_bot_settings.chat_emerg, message)
            self.bot.switch_bot_sell = False
            self.bot.save(update_fields=['switch_bot_sell'])

    def _release_btc(self, trade_obj):
        response = self.lbtc.contact_release(str(trade_obj.trade_id))
        if response.status_code == 200:
            return True
        else:
            return False

    def _is_trade_processed(self, con_id):
        for i in OpenTrades.objects.all():
            if con_id == i.trade_id:
                return True
        return False

    def send_first_message(self, trade_obj):
        qiwi = self._get_appropriate_qiwi(trade_obj.amount_rub)
        message = self.bot.greetings_text.format(qiwi.phone_number, trade_obj.reference_text)
        response = self.lbtc.post_message_to_contact(str(trade_obj.trade_id), message)
        if response.status_code == 200:
            trade_obj.api_key_qiwi = qiwi
            trade_obj.save(update_fields=['api_key_qiwi'])
            return True
        else:
            return False

    def send_second_message(self, trade_obj):
        response = self.lbtc.post_message_to_contact(str(trade_obj.trade_id), self.bot.farewell_text)
        if response.status_code == 200:
            return True
        else:
            return False

    def leave_review(self, trade_obj):
        response = self.lbtc.post_feedback_to_user(trade_obj.contragent, feedback='positive', message=self.bot.review_text)
        if response.status_code == 200:
            return True
        else:
            return False

    def check_dispute_result(self, my_trade):
        local_trade = self._get_specific_trade(my_trade.trade_id)
        if local_trade == None:
            return False

        if local_trade['data']['released_at']:
            message = 'Спор по сделке №{0} завершился отпуском битков. Проверьте, поступила ли оплата. Если нет, то сделку надо удалить из системы'.format(my_trade.trade_id)
            self.telegram_bot.send_message(self.bot.telegram_bot_settings.chat_emerg, message)
            self.make_new_deal(my_trade)
            my_trade.delete()
        elif local_trade['data']['closed_at']:
            my_trade.delete()

    def make_new_deal(self, my_trade):
        local_trade = self._get_specific_trade(my_trade.trade_id)
        if local_trade == None:
            return False

        rate_rub = Decimal(local_trade['data']['amount']) / (
                    Decimal(local_trade['data']['amount_btc']) + Decimal(local_trade['data']['fee_btc']))
        buy_rate = self.ad_upd._find_mean_buy_price()
        profit_rub_trade = (1 - (buy_rate / rate_rub)) * Decimal(local_trade['data']['amount'])
        profit_rub_trade -= profit_rub_trade * (self.bot.qiwi_profit_fee / 100)
        ReleasedTradesInfo.objects.create(ad_id=local_trade['data']['contact_id'],
                                          trade_type=local_trade['data']['advertisement']['trade_type'],
                                          payment_method=local_trade['data']['advertisement']['payment_method'],
                                          created_at=timezone.now(),
                                          released_at=local_trade['data']['released_at'],
                                          reference_code=local_trade['data']['reference_code'],
                                          contact_id=local_trade['data']['contact_id'],
                                          amount_rub=local_trade['data']['amount'],
                                          amount_btc=local_trade['data']['amount_btc'],
                                          fee_btc=local_trade['data']['fee_btc'],
                                          rate_rub=rate_rub,
                                          seller=local_trade['data']['seller']['username'],
                                          buyer=local_trade['data']['buyer']['username'],
                                          profit_rub_trade=profit_rub_trade,
                                          profit_rub_full=rate_rub - buy_rate,
                                          api_key_qiwi=my_trade.api_key_qiwi)
        self._reduce_buy_leftover(Decimal(local_trade['data']['amount_btc']) + Decimal(local_trade['data']['fee_btc']))
        my_trade.api_key_qiwi.limit_left -= Decimal(local_trade['data']['amount'])
        my_trade.api_key_qiwi.save(update_fileds=['limit_left'])
        my_trade.delete()

    def check_new_trades(self):
        if not self.opened_trades:
            self._get_opened_trades()
        if not self._get_all_notifications():
            self._get_all_notifications()
        btc_left_to_sell = Decimal('0')
        btc_opened_deals = Decimal('0')
        for i in MeanBuyTrades.objects.all():
            btc_left_to_sell += i.btc_amount

        if self.opened_trades:
            for i in self.opened_trades['data']['contact_list']:
                contact_id = i['data']['contact_id']
                ad_id = i['data']['advertisement']['id']
                if not i['data']['disputed_at'] and not self._is_trade_processed(contact_id) and ad_id == self.my_ad_info.ad_id:
                    reference_text = self.reference_text + i['data']['reference_code']
                    new_trade = OpenTrades.objects.create(trade_id=contact_id,
                                                          contragent=i['data']['buyer']['username'],
                                                          amount_rub=i['data']['amount'],
                                                          amount_btc=i['data']['amount_btc'],
                                                          created_at=timezone.now(),
                                                          reference_text=reference_text)
                    if self.send_first_message(new_trade):
                        new_trade.sent_first_message = True
                        new_trade.save(update_fields=['sent_first_message'])

                    for notification in self.all_notifications['data']:
                        if notification['contact_id'] == contact_id:
                            self.lbtc.mark_notification_as_read(str(notification['id']))
                            break
                if not i['data']['disputed_at']:
                    btc_opened_deals += (Decimal(i['data']['amount_btc']) + Decimal(i['data']['fee_btc']))
        if btc_opened_deals > btc_left_to_sell:
            message = 'Открытые сделки превышают оставшийся лимит по биткам. Продажа остановлена. По открытым сделкам битки будут отпущены автоматически, как только поступит оплата.'
            self.telegram_bot.send_message(self.bot.telegram_bot_settings.chat_emerg, message)
            self.bot.switch_bot_sell = False
            self.bot.save(update_fields=['switch_bot_sell'])


    def check_payment(self, my_trade):
        wallet = pyqiwi.Wallet(token=my_trade.api_key_qiwi.api_key,
                               proxy=my_trade.api_key_qiwi.proxy,
                               number=my_trade.api_key_qiwi.phone_number)
        payments = wallet.history(operation='IN', start_date=my_trade.created_at, end_date=timezone.now())
        local_trade = self._get_specific_trade(my_trade.trade_id)
        if local_trade == None:
            return None
        if local_trade['data']['canceled_at'] or (local_trade['data']['closed_at'] and not local_trade['data']['released_at']):
            my_trade.delete()
            return True
        if local_trade['data']['disputed_at']:
            message = 'По сделке №{0} открыт диспут {1}'.format(my_trade.id, local_trade['data']['disputed_at'])
            self.telegram_bot.send_message(self.bot.telegram_bot_settings.chat_emerg, message)
            my_trade.disputed = True
            my_trade.save(update_fields=['disputed'])
            return None
        for payment in payments['transactions']:
            if my_trade.reference_text in payment.comment and payment.sum.currency == 643 \
                    and payment.sum.amount == my_trade.amount_rub and not local_trade['data']['released_at']:
                if self._release_btc(my_trade):
                    my_trade.paid = True
                    my_trade.save(update_fields=['paid'])
                    self.make_new_deal(my_trade)
                    if self.send_second_message(my_trade):
                        my_trade.sent_second_message = True
                        my_trade.save(update_fields=['sent_second_message'])
                        if self.bot.switch_rev_send_sell:
                            if self.leave_review(my_trade):
                                my_trade.delete()
                                return True
                        else:
                            my_trade.delete()
                            return True
