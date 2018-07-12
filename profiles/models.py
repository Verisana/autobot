from django.db import models
from django.contrib.auth.models import AbstractUser


class Profile(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    api_key = models.ManyToManyField('profiles.APIKey')


class APIKey(models.Model):
    name = models.CharField(max_length=64)
    api_key = models.CharField(max_length=32)
    api_secret = models.CharField(max_length=64)
    username = models.ForeignKey('Profile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        text = '%s' % (self.name)
        return text


class APIKeyQiwi(models.Model):
    name = models.CharField(max_length=64)
    api_key = models.CharField(max_length=32)
    username = models.ForeignKey('Profile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        text = '%s' % (self.name)
        return text