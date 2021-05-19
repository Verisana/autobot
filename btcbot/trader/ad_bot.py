from datetime import timedelta
from decimal import *
from btcbot.models import BotSetting, MeanBuyTrades
from btcbot.trader.local_api import LocalBitcoin


class AdUpdateBot():
    STEP = 1
    FREQUENCY = timedelta(seconds=1.0)
    PRICE_ROUND = False


    def __init__(self, setting_id, proxy, sell_direction=True):
        self.bot = BotSetting.objects.get(id=setting_id)
        self.sell_direction = sell_direction
        self.proxy = proxy
        self.lbtc = LocalBitcoin('', '')
        self.ad_info = None
        if self.sell_direction:
            self.my_ad_info = self.bot.sell_ad_settings
        else:
            self.my_ad_info = self.bot.buy_ad_settings
        self.lbtc = LocalBitcoin(self.my_ad_info.api_key.api_key,
                                 self.my_ad_info.api_key.api_secret)
        self.mean_buy_price = self._find_mean_buy_price()
        self.stop_price = self._find_stop_price(Decimal(self.bot.target_profit), self.mean_buy_price, self.sell_direction)
        self.my_ad_info.stop_price = self.stop_price
        self.my_ad_info.save(update_fields=['stop_price'])
        self.volume_min = self.bot.volume_min
        self.volume_max = self.bot.volume_max

    def _find_mean_buy_price(self):
        mbt = MeanBuyTrades.objects.all()
        quant = Decimal('0.00000001')
        if len(mbt) == 1:
            return mbt[0].price_rub
        elif mbt:
            n = 0
            x = 0
            for i, item in enumerate(mbt):
                prod = int(round(item.btc_amount / quant, 0))
                n += 1 + prod
                x += item.price_rub * prod
            return Decimal(x / n)
        else:
            return None

    def _get_ad_info(self):
        if self.sell_direction:
            n = 0
            while n < 9:
                response = self.lbtc.get_sell_qiwi_ads(self.proxy)
                if response[0].status_code == 200 and response[1].status_code == 200:
                    self.ad_info = response[0].json()
                    if 'pagination' in self.ad_info:
                        ad_page_2 = response[1].json()
                        self.ad_info['data']['ad_list'].extend(ad_page_2['data']['ad_list'])
                    break
                n += 1
        else:
            n = 0
            while n < 9:
                response = self.lbtc.get_buy_qiwi_ads(self.proxy)
                if response[0].status_code == 200 and response[1].status_code == 200:
                    self.ad_info = response[0].json()
                    if 'pagination' in self.ad_info:
                        ad_page_2 = response[1].json()
                        self.ad_info['data']['ad_list'].extend(ad_page_2['data']['ad_list'])
                    break
                n += 1

    def _find_stop_price(self, profit, mean_buy, sell_direction):
        if sell_direction:
            stop_price = mean_buy + profit
            stop_price = stop_price + (stop_price * Decimal('0.01'))
            stop_price = stop_price + (profit * (self.bot.qiwi_profit_fee / 100))
            return stop_price
        else:
            return 0

    def _is_stop_triggered(self, price_comp, stop_price):
        if self.sell_direction:
            return price_comp <= stop_price
        else:
            return price_comp >= stop_price

    def _is_min_triggered(self, min_value_comp, min_value_bot):
        if min_value_bot != 0:
            return min_value_comp > min_value_bot
        else:
            return False

    def _is_max_triggered(self, max_value_comp, max_value_bot):
        if max_value_bot != 0:
            return max_value_comp < max_value_bot
        else:
            return False

    def _is_ad_filtered(self, curr_ad):
        price_comp = Decimal(curr_ad['data']['temp_price'])
        min_value_comp = int(curr_ad['data']['min_amount'])
        if min_value_comp == None:
            min_value_comp = 0
        max_value_comp = int(curr_ad['data']['max_amount_available'])

        return self._is_stop_triggered(price_comp, self.stop_price) \
                or self._is_min_triggered(min_value_comp, self.volume_min) \
                or self._is_max_triggered(max_value_comp, self.volume_max)

    def _is_first(self):
        result = {'is_first': None, 'compensate': 0}

        for i, item in enumerate(self.ad_info['data']['ad_list']):
            ad_id = item['data']['ad_id']
            if ad_id == self.my_ad_info.ad_id and i - result['compensate'] == 0:
                ads_below_me = self.ad_info['data']['ad_list'][i+1:]
                if not self._is_ad_filtered(ads_below_me[0]):
                    result['is_first'] = True
                    break
                else:
                    for l, item in enumerate(ads_below_me):
                        if self._is_ad_filtered(item):
                            result['compensate'] += 1
                        else:
                            result['is_first'] = True
                            break
                    break
            else:
                if not self._is_ad_filtered(item):
                    result['is_first'] = False
                    result['rival'] = i
                    break
                else:
                    result['compensate'] += 1
        return result

    def _update_price(self, rival):
        target_price = int()
        str_price = str()
        temp_price = Decimal(self.ad_info['data']['ad_list'][rival]['data']['temp_price'])
        if self.sell_direction:
            target_price = int(round(temp_price)) - self.STEP
            if self.PRICE_ROUND:
                while target_price % 100 > 0:
                    target_price -= 1
            if target_price < int(round(self.stop_price)):
                target_price = int(round(self.stop_price))
        else:
            target_price = int(round(temp_price)) + self.STEP
            if self.PRICE_ROUND:
                while target_price % 100 > 0:
                    target_price += 1
            if target_price > int(round(self.stop_price)):
                target_price = int(round(self.stop_price))
        str_price = str(target_price) + '.00'
        if target_price == self.my_ad_info.my_price:
            pass
        else:
            response = self.lbtc.update_equation(str(self.my_ad_info.ad_id), str_price)
            if response.status_code == 200:
                self.my_ad_info.my_price = target_price
                self.my_ad_info.save(update_fields=['my_price'])

    def check_ads(self):
        if not self.ad_info:
            self._get_ad_info()
        ad_visible = False
        for i in self.ad_info['data']['ad_list']:
            if i['data']['ad_id'] == self.my_ad_info.ad_id:
                ad_visible = True
                break
        if ad_visible:
            isfirst = self._is_first()
            if isfirst['is_first']:
                self._update_price(1+isfirst['compensate'])
            else:
                self._update_price(isfirst['rival'])
