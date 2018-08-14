from django.urls import path
from django.contrib.auth import views
from django.views import generic
from .views import IndexView, MessageView, SettingsView


app_name = 'btcbot'
urlpatterns = [
    path('index/', IndexView.as_view(), name='index'),
    path('messages/', MessageView.as_view(), name='message'),
    path('settings/', SettingsView.as_view(), name='settings'),

]