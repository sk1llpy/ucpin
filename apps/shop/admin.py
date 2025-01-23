from django.contrib import admin
from unfold import admin as unfold
from .models import UCPackage, RedeemCode, Purchase
from apps.users.models import User


# Админ для модели UCPackage
class UCPackageAdmin(unfold.ModelAdmin):
    list_display = ('title', 'price_usd', 'price_uzs',)
    search_fields = ('title',)
    list_filter = ('price_usd', 'price_uzs')
    ordering = ('title',)
    fieldsets = (
        (None, {
            'fields': ('title',)
        }),
        ("Цена", {
            'fields': ('price_usd', 'price_uzs'),
            'classes': ('collapse',)
        })
    )

    def __str__(self):
        return f"{self.title} ({self.price_usd} USD / {self.price_uzs} UZS)"

    class Meta:
        verbose_name = 'Пакет'
        verbose_name_plural = 'Пакеты'


# Админ для модели RedeemCode
class RedeemCodeAdmin(unfold.ModelAdmin):
    list_display = ('code', 'package', 'is_used', 'package_title',)
    search_fields = ('code',)
    list_filter = ('package__title', 'is_used',)
    ordering = ('-is_used',)
    fieldsets = (
        (None, {
            'fields': ('code', 'package', 'is_used')
        }),
        ('Статус', {
            'fields': ('get_usage_status',),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('get_usage_status',)

    def package_title(self, obj):
        return obj.package.title
    package_title.short_description = 'Название пакета'

    def get_usage_status(self, obj):
        return "Использован" if obj.is_used else "Не использован"
    get_usage_status.short_description = 'Статус использования'

    def __str__(self):
        return f"Код {self.code} - Пакет {self.package.title}"

    class Meta:
        verbose_name = 'Код для обмена'
        verbose_name_plural = 'Коды для обмена'


# Админ для модели Purchase
class PurchaseAdmin(unfold.ModelAdmin):
    list_display = ('account', 'redeem_code', 'balance_type',)
    list_filter = ('balance_type', 'account')
    ordering = ('-id',)
    fieldsets = (
        (None, {
            'fields': ('account', 'redeem_code', 'balance_type')
        }),
    )

    def __str__(self):
        return f"Покупка {self.account.email} - Код: {self.redeem_code.code}"

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'


# Регистрация моделей с их кастомными админами
admin.site.register(UCPackage, UCPackageAdmin)
admin.site.register(RedeemCode, RedeemCodeAdmin)
admin.site.register(Purchase, PurchaseAdmin)
