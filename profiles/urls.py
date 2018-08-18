from django.urls import path
from django.contrib.auth import views
from .views import WalletsView, EditorView


app_name = 'profiles'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('wallets/', WalletsView.as_view(), name='wallets'),
    path('editor/', EditorView.as_view(), name='editor'),
]
