from decimal import *
from celery import shared_task
import pytz
from django.utils import timezone
from info_data.models import ReleasedTradesInfo
from btcbot.models import BotSetting
from profiles.tasks import qiwi_limit_resetter
import telegram


@shared_task
def daily_routine_starter():
    qiwi_limit_resetter()
    daily_report_handler()

@shared_task
def daily_report_handler(full=True):
    sum_sell_rub = Decimal('0.0')
    sum_sell_btc = Decimal('0.0')
    mean_sell_price = Decimal('0.0')
    num_trades_sell = int()
    sum_buy_rub = Decimal('0.0')
    sum_buy_btc = Decimal('0.0')
    mean_buy_price = Decimal('0.0')
    num_trades_buy = int()

    bot_set = BotSetting.objects.get(name='Bot_QIWI')
    telegram_bot = telegram.Bot(token=bot_set.telegram_bot_settings.token)

    year = timezone.now().astimezone().year
    month = timezone.now().astimezone().month
    if full:
        day = timezone.now().astimezone().day - 1
    else:
        day = timezone.now().astimezone().day

    released_trades_24h = ReleasedTradesInfo.objects.filter(created_at__year=year,
                                                            created_at__month=month,
                                                            created_at__day=day)
    if released_trades_24h:
        profit = Decimal('0.0')
        for trades in released_trades_24h:
            if trades.trade_type == 'ONLINE_SELL':
                sum_sell_rub += trades.amount_rub
                sum_sell_btc += (trades.amount_btc + trades.fee_btc)
                num_trades_sell += 1
                profit += trades.profit_rub_trade
            elif trades.trade_type == 'ONLINE_BUY':
                sum_buy_rub += trades.amount_rub
                sum_buy_btc += (trades.amount_btc + trades.fee_btc)
                num_trades_buy += 1

        if sum_sell_btc:
            mean_sell_price = round(sum_sell_rub / sum_sell_btc, 2)
        if sum_buy_btc:
            mean_buy_price = round(sum_buy_rub / sum_buy_btc, 2)

        text = '''Суточный отчет по торговле битками от {0}.{1}.{2}
        
    Закуп:
    {3} - всего в рублях
    {4} - всего в битках
    {5} - средний курс
    {6} - количество сделок
            
    Продажи:
    {7} - всего в рублях
    {8} - всего в битках
    {9} - средний курс
    {10} - количество сделок
            
    {11} - профит'''
        message = text.format(day, month, year, sum_buy_rub, sum_buy_btc, mean_buy_price, num_trades_buy,
                              sum_sell_rub, sum_sell_btc, mean_sell_price, num_trades_sell, profit)
        telegram_bot.send_message(bot_set.telegram_bot_settings.chat_report, message)