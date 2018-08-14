from django.urls import path
from django.contrib.auth import views
from django.views import generic
from .views import WalletsView


app_name = 'profiles'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('wallets/', WalletsView.as_view(), name='wallets'),
]
