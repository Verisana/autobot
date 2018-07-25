from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    pass


class APIKey(models.Model):
    name = models.CharField(max_length=64)
    api_key = models.CharField(max_length=32)
    api_secret = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return '%s' % self.name


class APIKeyQiwi(models.Model):
    name = models.CharField(max_length=64)
    api_key = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=11)
    proxy = models.CharField(max_length=25, null=True, blank=True)
    bank_card = models.CharField(max_length=32, blank=True, null=True)
    pay_system = models.CharField(max_length=64,
                                  choices=(('1963', 'Visa'),
                                           ('21013', 'MasterCard')),
                                  blank=True, null=True)
    limit_left = models.DecimalField(max_digits=9, decimal_places=2, null=True, default=0)
    balance = models.DecimalField(max_digits=9, decimal_places=2, blank=True, null=True)
    used_at = models.DateTimeField(blank=True, null=True)
    is_blocked = models.BooleanField(default=False)
    def __str__(self):
        return '{0}: {1}, {2}'.format(self.name, self.is_blocked, self.balance)

class TelegramBotSettings(models.Model):
    name = models.CharField(max_length=64)
    token = models.CharField(max_length=64)
    chat_emerg = models.CharField(max_length=32)
    chat_report = models.CharField(max_length=32)
    proxy = models.CharField(max_length=25, blank=True, null=True)
    def __str__(self):
        return '%s' % self.name