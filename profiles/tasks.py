from decimal import *
from celery import shared_task
from info_data.models import ReleasedTradesInfo, UsedTransactions
from .models import APIKeyQiwi
import telegram
from btcbot.models import BotSetting, OpenTrades
from btcbot.qiwi_api import pyqiwi


@shared_task
def qiwi_status_updater():
    qiwis = APIKeyQiwi.objects.filter(is_blocked=False)
    bot_set = BotSetting.objects.get(name='Bot_QIWI')
    telegram_bot = telegram.Bot(token=bot_set.telegram_bot_settings.token)
    for qiwi in qiwis:
        wallet = pyqiwi.Wallet(token=qiwi.api_key,
                               proxy=qiwi.proxy,
                               number=qiwi.phone_number)
        try:
            qiwi.balance = wallet.balance()
            qiwi.is_blocked = wallet.profile.contract_info.blocked
            qiwi.save()
        except APIError:
            qiwi.is_blocked = True
            qiwi.save()
            message = 'Киви кошелек +{0}, скорее всего, блокнут. Баланс: {1}'.format(qiwi.phone_number, qiwi.balance)
            self.telegram_bot.send_message(self.bot.telegram_bot_settings.chat_emerg, message)
            continue

        if qiwi.is_blocked:
            message = 'Киви кошелек +{0} блокнут. Баланс: {1}'.format(qiwi.phone_number, qiwi.balance)
            telegram_bot.send_message(bot_set.telegram_bot_settings.chat_emerg, message)

@shared_task
def qiwi_limit_resetter():
    bot_set = BotSetting.objects.get(name='Bot_QIWI')
    qiwis = APIKeyQiwi.objects.all()
    transactions = UsedTransactions.objects.all().order_by('-created_at')

    for qiwi in qiwis:
        if qiwi.is_blocked:
            qiwi.limit_left = 0
            qiwi.save()
        else:
            qiwi.limit_left = bot_set.qiwi_limit
            qiwi.save()

    if len(transactions) > 100:
        for transaction in transactions[100:]:
            transaction.delete()


@shared_task
def qiwi_profit_fixator():
    qiwis_profit = APIKeyQiwi.objects.filter(for_profit_fixation=True)

    bot_set = BotSetting.objects.get(name='Bot_QIWI')
    telegram_bot = telegram.Bot(token=bot_set.telegram_bot_settings.token)
    overall_profit = Decimal('0.0')

    if bot_set.switch_profit_fixator:
        for qiwi in qiwis_profit:
            profit = Decimal('0.0')
            wallet = pyqiwi.Wallet(token=qiwi.api_key,
                                   proxy=qiwi.proxy,
                                   number=qiwi.phone_number)
            #workaround to choose current person and get all trades of all qiwi wallets
            proxy = qiwi.proxy
            qiwis_person = APIKeyQiwi.objects.filter(proxy=proxy)
            for qiwi_person in qiwis_person:
                trades = ReleasedTradesInfo.objects.filter(api_key_qiwi=qiwi_person)
                for trade in trades:
                    if qiwi.is_blocked:
                        trade.is_qiwi_blocked = True
                        trade.save()
                    else:
                        if trade.trade_type == 'ONLINE_SELL':
                            profit += trade.profit_rub_trade
            if not qiwi.is_blocked and profit > 0:
                response = wallet.send(pid=qiwi.pay_system, recipient=str(qiwi.bank_card), amount=profit)
                if response.transaction.state == 'Accepted':
                    for trade in trades:
                        trade.is_profit_fixated = True
                        trade.save()
                else:
                    message = 'Не удалось вывести прибыль с киви в размере {1} руб. Проверьте статус платежа на киви: +{0}'.format(qiwi.phone_number, profit)
                    telegram_bot.send_message(bot_set.telegram_bot_settings.chat_emerg, message)
            overall_profit += profit

        message = 'Вся прибыль по проданым биткам зафиксирована. Сумма выведенных средств: {0} руб.'.format(overall_profit)
        telegram_bot.send_message(bot_set.telegram_bot_settings.chat_emerg, message)