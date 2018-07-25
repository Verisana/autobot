from decimal import *
from celery import shared_task
from info_data.models import ReleasedTradesInfo
from .models import APIKeyQiwi
import telegram
from btcbot.models import BotSetting, OpenTrades
from btcbot.qiwi_api import pyqiwi


@shared_task
def qiwi_status_updater():
    qiwis = APIKeyQiwi.objects.filter(is_blocked=False)
    bot_set = BotSetting.objects.get(name='Bot_QIWI')
    if bot_set.switch_qiwi_updater:
        for qiwi in qiwis:
            wallet = pyqiwi.Wallet(token=qiwi.api_key,
                                   proxy=qiwi.proxy,
                                   number=qiwi.phone_number)
            qiwi.balance = wallet.balance()
            qiwi.is_blocked = wallet.profile.contract_info.blocked
            qiwi.save(update_fields=['balance', 'is_blocked'])


@shared_task
def qiwi_limit_resetter():
    bot_set = BotSetting.objects.get(name='Bot_QIWI')
    qiwis = APIKeyQiwi.objects.all()
    for qiwi in qiwis:
        if qiwi.is_blocked:
            qiwi.limit_left = 0
            qiwi.save(update_fields=['limit_left'])
        else:
            qiwi.limit_left = bot_set.qiwi_limit
            qiwi.save(update_fields=['limit_left'])


@shared_task
def qiwi_profit_fixator():
    qiwis = APIKeyQiwi.objects.all()
    bot_set = BotSetting.objects.get(name='Bot_QIWI')
    telegram_bot = telegram.Bot(token=bot_set.telegram_bot_settings.token)
    overall_profit = Decimal('0.0')

    if bot_set.switch_profit_fixator:
        for qiwi in qiwis:
            profit = Decimal('0.0')
            wallet = pyqiwi.Wallet(token=qiwi.api_key,
                                   proxy=qiwi.proxy,
                                   number=qiwi.phone_number)
            trades = ReleasedTradesInfo.objects.filter(api_key_qiwi=qiwi)
            for trade in trades:
                if qiwi.is_blocked:
                    trade.is_qiwi_blocked = True
                    trade.save(update_fields=['is_qiwi_blocked'])
                else:
                    if trade.trade_type == 'ONLINE_SELL':
                        profit += trade.profit_rub_trade

            if not qiwi.is_blocked and profit > 0:
                response = wallet.send(pid=qiwi.pay_system, recipient=str(qiwi.bank_card), amount=profit)
                if response.transaction.state == 'Accepted':
                    for trade in trades:
                        trade.is_profit_fixated = True
                        trade.save(update_fields=['is_profit_fixated'])
                else:
                    message = 'Не удалось вывести прибыль с киви в размере {1} руб. Проверьте статус платежа на киви: +{0}'.format(qiwi.phone_number, profit)
                    telegram_bot.send_message(bot_set.telegram_bot_settings.chat_emerg, message)
            overall_profit += profit

        message = 'Вся прибыль по проданым биткам зафиксирована. Сумма выведенных средств: {0} руб.'.format(overall_profit)
        telegram_bot.send_message(bot_set.telegram_bot_settings.chat_emerg, message)