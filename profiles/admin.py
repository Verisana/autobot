from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm
from .models import Profile, APIKey, APIKeyQiwi


class ProfileChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = Profile


class ProfileAdmin(UserAdmin):
    form = ProfileChangeForm

    fieldsets = UserAdmin.fieldsets + (
        ('Addition', {'fields': ('email_confirmed', 'api_key')}),
    )
    filter_horizontal = UserAdmin.filter_horizontal + ('api_key',)


class APIKeyAdmin(admin.ModelAdmin):
    fields = ['name', 'api_key', 'api_secret', 'username']
    list_display = ['name', 'username', 'api_key', 'api_secret', 'created_at']


class APIKeyQiwiAdmin(admin.ModelAdmin):
    fields = ['name', 'api_key', 'username']
    list_display = ['name', 'username', 'api_key', 'created_at']


admin.site.register(APIKey, APIKeyAdmin)
admin.site.register(APIKeyQiwi, APIKeyQiwiAdmin)
admin.site.register(Profile, ProfileAdmin)