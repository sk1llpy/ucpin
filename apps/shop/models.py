from django.db import models
from apps.general.models import BaseModel
from apps.general.choices import BalanceTypeChoices, PaymentTypeChoices
from apps.users.models import Account

# Модель UCPackage
class UCPackage(BaseModel):
    title = models.CharField(max_length=255, verbose_name="Название пакета")
    price_usd = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2, verbose_name="Цена в USD")
    price_uzs = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2, verbose_name="Цена в UZS")

    def __str__(self):
        return f"{self.title} ({self.price_usd} USD / {self.price_uzs} UZS)"

    class Meta:
        verbose_name = 'Пакет'
        verbose_name_plural = 'Пакеты'


# Модель RedeemCode
class RedeemCode(BaseModel):
    code = models.CharField(max_length=255, unique=True, verbose_name="Код обмена")
    package = models.ForeignKey(UCPackage, on_delete=models.CASCADE, verbose_name="Пакет")
    is_used = models.BooleanField(default=False, verbose_name="Использован")

    def __str__(self):
        return f"Код {self.code} - Пакет {self.package.title}"

    class Meta:
        verbose_name = 'Redeem Код'
        verbose_name_plural = 'Redeem Коды'


# Модель Purchase
class Purchase(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Пользователь")
    redeem_code = models.ForeignKey(RedeemCode, on_delete=models.CASCADE, verbose_name="Redeem Код")
    balance_type = models.CharField(
        max_length=255, blank=True, null=True, choices=BalanceTypeChoices, verbose_name="Тип баланса")

    def save(self, *args, **kwargs):
        self.redeem_code.is_used = True

        if self.balance_type == BalanceTypeChoices.usd:
            self.account.balance_usd -= self.redeem_code.package.price_usd
        elif self.balance_type == BalanceTypeChoices.uzs:
            self.account.balance_uzs -= self.redeem_code.package.price_uzs
        
        self.account.save()
        self.redeem_code.save()

        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Покупка {self.account.email} - Код: {self.redeem_code.code}"

    class Meta:
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'


class TopUp(BaseModel):
    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, verbose_name="Пользователь")
    amount = models.DecimalField(
        max_digits=12, decimal_places=2, verbose_name="Сумма")
    balance_type = models.CharField(
        max_length=255, 
        blank=True, null=True, 
        choices=BalanceTypeChoices.choices, 
        verbose_name="Тип баланса"
    )
    payment_type = models.CharField(
        max_length=255,
        blank=True, null=True,
        choices=PaymentTypeChoices.choices,
        verbose_name="Тип платежа"
    )
    verified = models.BooleanField(default=False, verbose_name="Проверено?")

    def save(self, *args, **kwargs):
        if self.verified:
            if self.balance_type == BalanceTypeChoices.usd:
                self.account.balance_usd += self.amount
            elif self.balance_type == BalanceTypeChoices.uzs:
                self.account.balance_uzs += self.amount
        
            self.account.save()
        
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"Пополнить счет - #{self.pk} ({self.account.full_name})"
    
    class Meta:
        verbose_name = "Пополнить счет"
        verbose_name_plural = "Пополнить счет"
