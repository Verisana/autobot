import pickle
import random
from celery import shared_task
from celery.task.control import inspect
from btcbot.models import BotSetting
from btcbot.trader.ad_bot import AdUpdateBot


@shared_task
def sell_ad_bot_execution(proxy_num):
    bot_settings = BotSetting.objects.get(name='Bot_QIWI')
    proxies_list = pickle.load(open('info_data/proxies_list.pickle', 'rb'))
    if proxy_num == 1:
        proxy = [proxies_list[0][1], proxies_list[2][1]]
    else:
        proxy = [proxies_list[1][1], proxies_list[3][1]]
    ad_bot = AdUpdateBot(bot_settings.id, proxy)
    ad_bot.check_ads()
    if bot_settings.switch_sell_ad_upd:
        if proxy_num == 1:
            proxy_num = 2
        else:
            proxy_num = 1
        sell_ad_bot_execution.delay(proxy_num)


@shared_task
def buy_ad_bot_execution(proxy_num):
    bot_settings = BotSetting.objects.get(name='Bot_QIWI')
    proxies_list = pickle.load(open('info_data/proxies_list.pickle', 'rb'))
    if proxy_num == 1:
        proxy = [proxies_list[4][1], proxies_list[6][1]]
    else:
        proxy = [proxies_list[5][1], proxies_list[7][1]]
    ad_bot = AdUpdateBot(bot_settings.id, proxy, sell_direction=False)
    ad_bot.check_ads()
    if bot_settings.switch_buy_ad_upd:
        if proxy_num == 1:
            proxy_num = 2
        else:
            proxy_num = 1
        buy_ad_bot_execution.delay(proxy_num)


@shared_task
def ad_bot_runner():
    bot_settings = BotSetting.objects.get(name='Bot_QIWI')
    insp = inspect()
    active = insp.active()

    if bot_settings.switch_sell_ad_upd:
        if 'sell_ad_bot_execution@ubuntu' in active.keys():
            if not active['sell_ad_bot_execution@ubuntu']:
                sell_ad_bot_execution.delay(random.sample([1, 2], 1))
    if bot_settings.switch_buy_ad_upd:
        if 'buy_ad_bot_execution@ubuntu' in active.keys():
            if not active['buy_ad_bot_execution@ubuntu']:
                buy_ad_bot_execution.delay(random.sample([1, 2], 1))