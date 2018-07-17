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
    proxies = set()
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]') and i.xpath('.//td[5][contains(text(),"elite proxy")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    with open('info_data/proxy_list.pickle', 'wb') as outfile:
        pickle.dump(proxies, outfile)