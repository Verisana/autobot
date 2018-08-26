import json
import dateparser
from decimal import *
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.utils import timezone
from .models import OpenTrades, BotSetting
from profiles.models import Profile
from info_data.models import OperatorsWorkingShift, ReleasedTradesInfo
from btcbot.trader.local_api import LocalBitcoin
from datetime import timedelta
import telegram


class IndexView(LoginRequiredMixin, generic.ListView):
    model = OpenTrades
    template_name = 'btcbot/index.html'
    login_url = '/profiles/login/'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs = qs.order_by('-created_at')
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['opened_shift'] = OperatorsWorkingShift.objects.all().order_by('-start_working').first()
        return context

class MessageView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'btcbot/messages.html'
    login_url = '/profiles/login/'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        trade = OpenTrades.objects.get(id=int(context['pk']))
        context['amount_rub'] = trade.amount_rub
        bot = BotSetting.objects.get(name='Bot_QIWI')
        lbtc = LocalBitcoin(bot.sell_ad_settings.api_key.api_key, bot.sell_ad_settings.api_key.api_secret)
        messages = lbtc.get_contact_messages(str(trade.trade_id))
        try:
            messages = messages.json()
        except json.decoder.JSONDecodeError:
            context['json_except'] = True
        if 'json_except' not in context.keys():
            context['trade_messages'] = []
            for i in messages['data']['message_list'][::-1]:
                i['created_at'] = dateparser.parse(i['created_at']).astimezone()
                i['sender']['last_online'] = dateparser.parse(i['sender']['last_online']).astimezone()
                i['is_verified'] = trade.is_verified
                context['trade_messages'].append(i)
        return self.render_to_response(context)

class SettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'btcbot/settings.html'
    login_url = '/profiles/login/'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['bot'] = BotSetting.objects.get(name='Bot_QIWI')
        bot = BotSetting.objects.get(name='Bot_QIWI')
        context['wallets'] = bot.api_key_qiwi.all().order_by('name')
        return self.render_to_response(context)

class EditorView(LoginRequiredMixin, generic.View):
    http_method = ['post']
    login_url = '/profiles/login/'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bot = BotSetting.objects.get(name='Bot_QIWI')
        self.lbtc = LocalBitcoin(self.bot.sell_ad_settings.api_key.api_key, self.bot.sell_ad_settings.api_key.api_secret)
        self.telegram_bot = telegram.Bot(token=self.bot.telegram_bot_settings.token)

    def post(self, request, *args, **kwargs):
        if request.POST.get('editor') == 'opentrade_paid':
            opentrade_id = int(request.POST.get('opentrade_id'))
            operator = Profile.objects.get(id=request.user.id)
            self._change_opentrade_paid(opentrade_id, operator=operator)
        elif request.POST.get('editor') == 'send_message':
            trade = OpenTrades.objects.get(id=int(request.POST.get('opentrade_id')))
            self.lbtc.post_message_to_contact(str(trade.trade_id), request.POST.get('message'))
            return redirect('btcbot:message', pk=trade.id)
        elif request.POST.get('editor') == 'download_attachment':
            url = request.POST.get('attachment_url').split('/')
            response = self.lbtc.get_trade_attachment(url[5], url[6])
            return HttpResponse(response, content_type=response.headers['Content-Type'])
        elif request.POST.get('editor') == 'switch_bot_sell_ad':
            if self.bot.switch_bot_sell:
                self.bot.switch_bot_sell = False
            else:
                self.bot.switch_bot_sell = True
            self.bot.save()
            return redirect('btcbot:settings')
        elif request.POST.get('editor') == 'change_target_profit':
            self.bot.target_profit = int(request.POST.get('target_profit'))
            self.bot.save()
            return redirect('btcbot:settings')
        elif request.POST.get('editor') == 'open_new_shift':
            OperatorsWorkingShift.objects.create(start_working=timezone.now().astimezone(),
                                                 operator=request.user)
            message = '''Смена оператора {0} открыта
{1}'''.format(request.user.get_username(), timezone.now().astimezone())
            self.telegram_bot.send_message(self.bot.telegram_bot_settings.chat_report, message)
        elif request.POST.get('editor') == 'close_opened_shift':
            shift = OperatorsWorkingShift.objects.get(id=int(request.POST.get('shift_id')))
            self._close_opened_shift(shift, request.user)
        return redirect('btcbot:index')

    def _change_opentrade_paid(self, opentrade_id, operator):
        trade = OpenTrades.objects.get(id=opentrade_id)
        if trade.marked_paid:
            trade.marked_paid = False
        else:
            trade.marked_paid = True
            trade.who_marked_paid = operator
        trade.save()

    def _close_opened_shift(self, shift, operator):
        trades = ReleasedTradesInfo.objects.filter(who_released_btc=operator).filter(created_at__range=[shift.start_working,
                                                                                                        timezone.now()])
        amount_btc, amount_rub, tot_sec, profit, mean_sell_price = Decimal('0.0'), Decimal('0.0'), 0, Decimal('0.0'), Decimal('0.0')
        for trade in trades:
            amount_rub += trade.amount_rub
            amount_btc += trade.amount_btc
            if trade.deal_processed_time:
                tot_sec += trade.deal_processed_time.total_seconds()
            profit += trade.profit_rub_trade
            mean_sell_price += trade.rate_rub

        if not trades:
            mean_deal = timedelta(0)
            mean_sell_price = 0
        else:
            mean_sec = tot_sec / len(trades)
            mean_deal = timedelta(seconds=round(mean_sec, 0))
            mean_sell_price = mean_sell_price / len(trades)

        shift.end_working = timezone.now().astimezone()
        shift.shift_duration = shift.end_working - shift.start_working
        shift.number_of_deals = len(trades)
        shift.amount_sell_btc = amount_btc
        shift.amount_sell_rub = amount_rub
        shift.mean_deal_processing = mean_deal
        shift.profit_rub = profit
        shift.save()
        message = '''Смена оператора {0} закрыта
{1}
        
Длительность смены:
{2}

Среднее время обработки:
{3}

Количество сделок:
{4}
       
Сумма в битках:
{5}

Сумма в рублях:
{6}

Средний курс продажи:
{7}
        
Профит:
{8}        
        '''.format(shift.operator,
                   timezone.now().astimezone(),
                   shift.shift_duration,
                   shift.mean_deal_processing,
                   shift.number_of_deals,
                   shift.amount_sell_btc,
                   shift.amount_sell_rub,
                   mean_sell_price,
                   shift.profit_rub)
        self.telegram_bot.send_message(self.bot.telegram_bot_settings.chat_report, message)