from django.contrib import admin
from .models import PowerMeter, CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'uuid', 'is_staff', 'is_active',)
    search_fields = ('username', 'email', 'uuid')
    readonly_fields = ('date_joined', 'last_login',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PowerMeter)