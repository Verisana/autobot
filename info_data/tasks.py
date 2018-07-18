import requests
import pickle
from django.utils import timezone
from celery import shared_task, task
from celery.task.control import inspect
from .models import AdInfo
from btcbot.models import BotSetting
from btcbot.local_api import LocalBitcoin


@shared_task
def ads_updater(option, proxy_num):
    proxies_list = pickle.load(open('info_data/proxies_list.pickle', 'rb'))
    lbtc = LocalBitcoin('', '')
    payment_method = 'qiwi'
    if option == 1:
        trade_direction = 'buy-bitcoins-online'
        page_number = '1'
        if proxy_num == 1:
            proxy = proxies_list[0][1]
        else:
            proxy = proxies_list[1][1]
    elif option == 2:
        trade_direction = 'buy-bitcoins-online'
        page_number = '2'
        if proxy_num == 1:
            proxy = proxies_list[2][1]
        else:
            proxy = proxies_list[3][1]
    elif option == 3:
        trade_direction = 'sell-bitcoins-online'
        page_number = '1'
        if proxy_num == 1:
            proxy = proxies_list[4][1]
        else:
            proxy = proxies_list[5][1]
    elif option == 4:
        trade_direction = 'sell-bitcoins-online'
        page_number = '2'
        if proxy_num == 1:
            proxy = proxies_list[6][1]
        else:
            proxy = proxies_list[7][1]
    response = lbtc.get_public_ads(trade_direction, payment_method, page_number, proxy)
    if response.status_code == 200:
        if page_number == '2' and 'pagination' not in response.json().keys():
            empty = {}
            with open('info_data/ad_info_%s.json' % str(option), 'w') as outfile:
                json.dump(empty, outfile)
            pass
        else:
            with open('info_data/ad_info_%.json' % str(option), 'w') as outfile:
                json.dump(response.json(), outfile)
    if BotSetting.objects.filter(switch=True):
        if proxy_num == 1:
            proxy_num_n = 2
        else:
            proxy_num_n = 1
        ads_updater.delay(option, proxy_num_n)

@shared_task
def ads_update_runner():
    if BotSetting.objects.filter(switch=True):
        for i in range(4):
            insp = inspect()
            reser = insp.reserved()
            active = insp.active()
            no_tasks = True

            if not reser == None and 'ad_updater@ubuntu-Assanix' in reser.keys():
                for l in reser['ad_updater@ubuntu-Assanix']:
                    if l['name'] == 'info_data.tasks.ad_updater' and i+1 == make_tuple(l['args'])[0]:
                        no_tasks = False
                        break
            if not active == None and 'ad_updater@ubuntu-Assanix' in active.keys():
                for l in active['ad_updater@ubuntu-Assanix']:
                    if l['name'] == 'info_data.tasks.ad_updater' and i+1 == make_tuple(l['args'])[0]:
                        no_tasks = False
                        break
            if no_tasks:
                ads_updater.delay(i+1, 1)