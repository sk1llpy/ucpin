from django.contrib import admin
from django.contrib.auth.models import User as BaseUser
from django.contrib.auth.models import Group as BaseGroup

from unfold import admin as unfold
from .models import User, Admin, Account


class UserAdmin(unfold.ModelAdmin):
    list_display = ('user_id', 'full_name', 'username', 'is_logined', 'created_at', 'updated_at')
    list_filter = ('is_logined', 'is_active')
    search_fields = ('user_id', 'full_name', 'username',)
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('user_id', 'username', 'account', )
        }),
        ('Статус аккаунта', {
            'fields': ('is_logined', 'is_active',)
        }),
        ('О дате и времени', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at',)


class AccountAdmin(unfold.ModelAdmin):
    list_display = ('email', 'phone_number', 'balance_usd', 'balance_uzs', 'created_at', 'updated_at')
    list_filter = ('is_active', 'is_banned')
    search_fields = ('email', 'phone_number',)
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('email', 'phone_number',)
        }),
        ('Статус аккаунта', {
            'fields': ('is_banned', 'is_active',)
        }),
        ('Баланс', {
            'fields': ('balance_usd', 'balance_uzs',)
        }),
        ('О дате и времени', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at',)


class AdminAdmin(unfold.ModelAdmin):
    list_display = ('account',)
    search_fields = ('account__email', 'account__phone_number')
    ordering = ('account__email',)
    fieldsets = (
        (None, {
            'fields': ('account',)
        }),
    )

# Регистрация моделей с кастомными интерфейсами администратора
admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Admin, AdminAdmin)

admin.site.unregister(BaseGroup)
