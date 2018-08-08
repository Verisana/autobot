from decimal import *
from celery import shared_task
from info_data.models import ReleasedTradesInfo
from .models import APIKeyQiwi
import telegram
from btcbot.models import BotSetting, OpenTrades
from btcbot.qiwi_api import pyqiwi


@shared_task
def qiwi_limit_resetter():
    bot_set = BotSetting.objects.get(name='Bot_QIWI')
    qiwis = APIKeyQiwi.objects.all()
    for qiwi in qiwis:
        if qiwi.is_blocked:
            qiwi.limit_left = 0
            qiwi.save()
        else:
            qiwi.limit_left = bot_set.qiwi_limit
            qiwi.save()