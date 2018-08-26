from decimal import *
from django.views import generic
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from .models import APIKeyQiwi
from btcbot.models import BotSetting


class WalletsView(LoginRequiredMixin, generic.ListView):
    model = APIKeyQiwi
    template_name = 'registration/wallets.html'
    login_url = '/profiles/login/'

    def get_queryset(self, **kwargs):
        qs = super().get_queryset(**kwargs)
        qs = qs.order_by('name')
        return qs


class EditorView(LoginRequiredMixin, generic.View):
    http_method = ['post']
    login_url = '/profiles/login/'

    def post(self, request, *args, **kwargs):
        qiwi_id = int(request.POST.get('qiwi_id'))
        if request.POST.get('editor') == 'qiwi_wallet_blocked':
            self._change_qiwi_blocked(qiwi_id)
        elif request.POST.get('editor') == 'qiwi_wallet_balance':
            balance = Decimal(request.POST.get('qiwi_balance'))
            self._change_qiwi_balance(qiwi_id, balance)
        elif request.POST.get('editor') == 'limit_resetter':
            self._limit_resetter(qiwi_id)
        return redirect('profiles:wallets')

    def _change_qiwi_blocked(self, qiwi_id):
        qiwi = APIKeyQiwi.objects.get(id=qiwi_id)

        if qiwi.is_blocked:
            qiwi.is_blocked = False
        else:
            qiwi.is_blocked = True
        qiwi.save()

    def _change_qiwi_balance(self, qiwi_id, balance):
        qiwi = APIKeyQiwi.objects.get(id=qiwi_id)
        qiwi.balance = balance
        qiwi.balance_edited_at = timezone.now().astimezone()
        qiwi.save()

    def _limit_resetter(self, qiwi_id):
        bot = BotSetting.objects.get(name='Bot_QIWI')
        qiwi = APIKeyQiwi.objects.get(id=qiwi_id)
        qiwi.limit_left = bot.qiwi_limit
        qiwi.save()