from btcbot.models import BotSetting, OpenTrades, MeanBuyTrades, AdSetting
from btcbot.trader.seller_bot import LocalSellerBot
from btcbot.trader.ad_bot import AdUpdateBot
from btcbot.trader.local_api import LocalBitcoin
from btcbot.tasks import seller_bot_handler
from profiles.models import APIKeyQiwi, TelegramBotSettings
from profiles.tasks import qiwi_status_updater, qiwi_limit_resetter, qiwi_profit_fixator
import telegram

bot_set = BotSetting.objects.get(name='Bot_QIWI')
seller = LocalSellerBot(bot_set.id)
pp = telegram.utils.request.Request(proxy_url='https://10.0.2.2:1080')
telegram = telegram.Bot(token=bot_set.telegram_bot_settings.token, request=pp)