import requests
import pickle
import datetime
from celery import shared_task, task
from celery.task.control import inspect
from .models import AdInfo
from btcbot.models import BotSetting
from btcbot.local_api import LocalBitcoin

@shared_task
def ad_updater(option, proxy_num):
    proxies_list = pickle.load(open('info_data/proxies_list.pickle', 'rb'))
    lbtc = LocalBitcoin('', '')
    payment_method = 'qiwi'
    if option == 1:
        trade_direction = 'buy-bitcoins-online'
        trade_filter = 'ONLINE_SELL'
        page_number = '1'
        if proxy_num == 1:
            proxy = proxies_list[0][1]
        else:
            proxy = proxies_list[1][1]
    elif option == 2:
        trade_direction = 'buy-bitcoins-online'
        trade_filter = 'ONLINE_SELL'
        page_number = '2'
        if proxy_num == 1:
            proxy = proxies_list[2][1]
        else:
            proxy = proxies_list[3][1]
    elif option == 3:
        trade_direction = 'sell-bitcoins-online'
        trade_filter = 'ONLINE_BUY'
        page_number = '1'
        if proxy_num == 1:
            proxy = proxies_list[4][1]
        else:
            proxy = proxies_list[5][1]
    elif option == 4:
        trade_direction = 'sell-bitcoins-online'
        trade_filter = 'ONLINE_BUY'
        page_number = '2'
        if proxy_num == 1:
            proxy = proxies_list[6][1]
        else:
            proxy = proxies_list[7][1]
    response = lbtc.get_public_ads(trade_direction, payment_method, page_number, proxy)
    if page_number == '2' and 'pagination' not in response.json().keys():
        pass
    else:
        my_ad_list = AdInfo.objects.filter(trade_type=trade_filter).filter(page_number=page_number)
        if my_ad_list:
            for i in my_ad_list:
                i.delete()
        get_ad_list = response.json()['data']['ad_list']
        for i, item in enumerate(get_ad_list):
            AdInfo.objects.create(contragent=item['data']['profile']['username'],
                                  updated_at=datetime.datetime.now(),
                                  trade_type=item['data']['trade_type'],
                                  ad_id=item['data']['ad_id'],
                                  price=item['data']['temp_price'],
                                  payment_window=item['data']['payment_window_minutes'],
                                  min_amount=item['data']['min_amount'],
                                  max_amount=item['data']['max_amount_available'],
                                  price_usd=item['data']['temp_price_usd'],
                                  payment_method='QIWI',
                                  page_number=page_number,
                                  order_number=i+1,
                                )

@shared_task
def ads_update_runner():
    if BotSetting.objects.filter(switch=True):
        for i in range(4):
            active = pickle.load(open('info_data/status_%s.pickle' % str(i+1), 'rb'))
            if not active[0]:
                active[0] = True
                #change proxy server
                if active[1] == 1:
                    active[1] = 2
                else:
                    active[1] = 1
                with open('info_data/status_%s.pickle' % str(i+1), 'wb') as outfile:
                    pickle.dump(active, outfile)
                ad_updater.delay(i+1, active[1])