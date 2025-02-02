from django.contrib import admin
from django.contrib.auth.models import User as BaseUser
from django.contrib.auth.models import Group as BaseGroup
from django.utils.translation import gettext_lazy as _

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

class BaseUserAdmin(unfold.ModelAdmin):
    list_display = ("id", "username", "email", "first_name", "last_name", "is_active", "is_staff", "is_superuser")
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined")
    search_fields = ("username", "email", "first_name", "last_name")
    ordering = ("-date_joined",)

    fieldsets = (
        (_("Личная информация"), {"fields": ("username", "email", "first_name", "last_name")}),
        (_("Конфиденциальность данных"), {"fields": ("password", )}),
        (_("Статус и права доступа"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Важные даты"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (_("Создание пользователя"), {
            "classes": ("wide",),
            "fields": ("username", "email", "first_name", "last_name"),
        }),
        (_("Конфиденциальность данных"), {
            "fields": ("password", )
        }),
    )

    readonly_fields = ("last_login", "date_joined")

# Регистрация моделей с кастомными интерфейсами администратора
admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Admin, AdminAdmin)

admin.site.unregister(BaseGroup)
admin.site.unregister(BaseUser)

admin.site.register(BaseUser, BaseUserAdmin)






