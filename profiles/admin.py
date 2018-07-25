from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import Profile, APIKey, APIKeyQiwi, TelegramBotSettings


class ProfileChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Profile


class ProfileAdmin(UserAdmin):
    form = ProfileChangeForm


class APIKeyAdmin(admin.ModelAdmin):
    # Include all fields except id and created_at
    fields = [field.name for field in APIKey._meta.fields if field.name != 'id' and field.name != 'created_at']
    list_display = [field.name for field in APIKey._meta.fields if field.name != 'id']


class APIKeyQiwiAdmin(admin.ModelAdmin):
    fields = [field.name for field in APIKeyQiwi._meta.fields if field.name != 'id' and field.name != 'created_at']
    list_display = [field.name for field in APIKeyQiwi._meta.fields if field.name != 'id' and field.name != 'api_key']


class TelegramBotSettingsAdmin(admin.ModelAdmin):
    fields = [field.name for field in TelegramBotSettings._meta.fields if field.name != 'id']
    list_display = [field.name for field in TelegramBotSettings._meta.fields if field.name != 'id']


admin.site.register(APIKey, APIKeyAdmin)
admin.site.register(APIKeyQiwi, APIKeyQiwiAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(TelegramBotSettings, TelegramBotSettingsAdmin)