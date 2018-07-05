from django.urls import path
from django.contrib.auth import views
from .views import ProfileSignUp, ProfilePasswordResetView, activate
from django.views import generic


app_name = 'profiles'
urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('password_change/', views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', ProfilePasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('signup/', ProfileSignUp.as_view(), name='signup'),

    path('account_activation_sent/', generic.TemplateView.as_view(template_name='registration/account_activation_email_sent.html'), name='account_activation_sent'),
    path('activate/<uidb64>/<token>/', activate, name='activate')
]
