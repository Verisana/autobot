from django.contrib import admin
from django.urls import path, reverse
from django.conf.urls import include
from django.conf import settings
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='btcbot:index')),
    path('btcbot/', include('btcbot.urls')),
    path('profiles/', include('profiles.urls')),
]

admin.site.site_header = 'AutoBot Administration'

admin.site.site_header = 'LocalBitcoins_bot Administration'
