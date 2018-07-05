from django.contrib import admin
from django.urls import path, reverse
from django.conf.urls import include
from django.conf import settings
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='admin:index')),
]

admin.site.site_header = 'LocalBitcoins_bot Administration'
