import requests
import pickle
from lxml.html import fromstring
from celery import shared_task, task
from celery.task.control import inspect
from .models import AdInfo


@shared_task
def proxy_list_scrapper():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = list()
    fast_proxies = list()

    for i in parser.xpath('//tbody/tr'):
        if (i.xpath('.//td[7][contains(text(),"yes")]') and i.xpath('.//td[5][contains(text(),"elite proxy")]')) and (
                                                                i.xpath('.//td[3][contains(text(), "RU")]') \
                                                                or i.xpath('.//td[3][contains(text(), "US")]') \
                                                                or i.xpath('.//td[3][contains(text(), "DE")]')):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.append(proxy)
    print(len(proxies))

    time_limit = 1.0
    while len(fast_proxies) < 8:
        for i, item in enumerate(proxies):
            try:
                response = requests.get('https://localbitcoins.net/', proxies={'http': item, 'https': item}, timeout=5)
            except:
                print("%d Skipping. Connnection error: %s" % (i, item))
                continue
            if response.status_code == 200 and response.elapsed.total_seconds() < time_limit:
                print('%d time: %s, country: %s' % (i, response.elapsed.total_seconds(), item))
                fast_proxies.append(item)
                proxies.pop(i)
                if len(fast_proxies) >= 8:
                    break
        time_limit += 0.5
        print(len(proxies))

    print(len(fast_proxies))
    with open('info_data/fast_proxies.pickle', 'wb') as outfile:
        pickle.dump(fast_proxies, outfile)


@shared_task
def ads_update_runner():
    pass