from celery import shared_task, task
from celery.task.control import inspect
from btcbot.models import BotSetting
from btcbot.ad_bot import AdUpdateBot


@shared_task
def sell_ad_bot_execution():
    bot_settings = BotSetting.objects.get(name='Bot_QIWI')
    ad_bot = AdUpdateBot(bot_settings.id)
    ad_bot.check_ads()
    if bot_settings.switch_sell_ad_upd:
        sell_ad_bot_execution.delay()


@shared_task
def buy_ad_bot_execution():
    bot_settings = BotSetting.objects.get(name='Bot_QIWI')
    ad_bot = AdUpdateBot(bot_settings.id, sell_direction=False)
    ad_bot.check_ads()
    if bot_settings.switch_buy_ad_upd:
        buy_ad_bot_execution.delay()


@shared_task
def ad_bot_runner():
    bot_settings = BotSetting.objects.get(name='Bot_QIWI')
    insp = inspect()
    active = insp.active()

    if bot_settings.switch_sell_ad_upd:
        if 'sell_ad_bot_execution@ubuntu' in active.keys():
            if not active['sell_ad_bot_execution@ubuntu']:
                sell_ad_bot_execution.delay()
    if bot_settings.switch_buy_ad_upd:
        if 'buy_ad_bot_execution@ubuntu' in active.keys():
            if not active['buy_ad_bot_execution@ubuntu']:
                buy_ad_bot_execution.delay()