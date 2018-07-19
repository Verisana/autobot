import requests
import pickle
import json
from django.utils import timezone
from celery import shared_task, task
from celery.task.control import inspect
from btcbot.models import BotSetting
from btcbot.local_api import LocalBitcoin


@shared_task
def ads_updater_1(proxy_num):
    proxies_list = pickle.load(open('info_data/proxies_list.pickle', 'rb'))
    lbtc = LocalBitcoin('', '')
    payment_method = 'qiwi'
    trade_direction = 'buy-bitcoins-online'
    page_number = '1'
    if proxy_num == 1:
        proxy = proxies_list[0][1]
    else:
        proxy = proxies_list[1][1]

    response = lbtc.get_public_ads(trade_direction, payment_method, page_number, proxy)
    if response.status_code == 200:
        with open('info_data/ad_info_1.json', 'w') as outfile:
            json.dump(response.json(), outfile)

    if BotSetting.objects.filter(switch=True):
        if proxy_num == 1:
            proxy_num = 2
        else:
            proxy_num = 1
        ads_updater_1.delay(proxy_num)


@shared_task
def ads_updater_2(proxy_num):
    proxies_list = pickle.load(open('info_data/proxies_list.pickle', 'rb'))
    lbtc = LocalBitcoin('', '')
    payment_method = 'qiwi'
    trade_direction = 'buy-bitcoins-online'
    page_number = '2'
    if proxy_num == 1:
        proxy = proxies_list[2][1]
    else:
        proxy = proxies_list[3][1]

    response = lbtc.get_public_ads(trade_direction, payment_method, page_number, proxy)
    if response.status_code == 200:
        if 'pagination' not in response.json().keys():
            empty = {'data': {'ad_list': []}}
            with open('info_data/ad_info_2.json', 'w') as outfile:
                json.dump(empty, outfile)
        else:
            with open('info_data/ad_info_2.json', 'w') as outfile:
                json.dump(response.json(), outfile)

    if BotSetting.objects.filter(switch=True):
        if proxy_num == 1:
            proxy_num = 2
        else:
            proxy_num = 1
        ads_updater_2.delay(proxy_num)


@shared_task
def ads_updater_3(proxy_num):
    proxies_list = pickle.load(open('info_data/proxies_list.pickle', 'rb'))
    lbtc = LocalBitcoin('', '')
    payment_method = 'qiwi'
    trade_direction = 'sell-bitcoins-online'
    page_number = '1'
    if proxy_num == 1:
        proxy = proxies_list[4][1]
    else:
        proxy = proxies_list[5][1]

    response = lbtc.get_public_ads(trade_direction, payment_method, page_number, proxy)
    if response.status_code == 200:
        with open('info_data/ad_info_3.json', 'w') as outfile:
            json.dump(response.json(), outfile)

    if BotSetting.objects.filter(switch=True):
        if proxy_num == 1:
            proxy_num = 2
        else:
            proxy_num = 1
        ads_updater_3.delay(proxy_num)


@shared_task
def ads_updater_4(proxy_num):
    proxies_list = pickle.load(open('info_data/proxies_list.pickle', 'rb'))
    lbtc = LocalBitcoin('', '')
    payment_method = 'qiwi'
    trade_direction = 'sell-bitcoins-online'
    page_number = '2'
    if proxy_num == 1:
        proxy = proxies_list[6][1]
    else:
        proxy = proxies_list[7][1]

    response = lbtc.get_public_ads(trade_direction, payment_method, page_number, proxy)
    if response.status_code == 200:
        if 'pagination' not in response.json().keys():
            empty = {'data': {'ad_list': []}}
            with open('info_data/ad_info_4.json', 'w') as outfile:
                json.dump(empty, outfile)
        else:
            with open('info_data/ad_info_4.json', 'w') as outfile:
                json.dump(response.json(), outfile)

    if BotSetting.objects.filter(switch=True):
        if proxy_num == 1:
            proxy_num = 2
        else:
            proxy_num = 1
        ads_updater_4.delay(proxy_num)


@shared_task
def ads_update_runner():
    if BotSetting.objects.filter(switch=True):
        insp = inspect()
        active = insp.active()
        if 'ads_updater_1@ubuntu' in active.keys():
            if not active['ads_updater_1@ubuntu']:
                ads_updater_1.delay(1)
        if 'ads_updater_2@ubuntu' in active.keys():
            if not active['ads_updater_2@ubuntu']:
                ads_updater_2.delay(1)
        if 'ads_updater_3@ubuntu' in active.keys():
            if not active['ads_updater_3@ubuntu']:
                ads_updater_3.delay(1)
        if 'ads_updater_4@ubuntu' in active.keys():
            if not active['ads_updater_4@ubuntu']:
                ads_updater_4.delay(1)
