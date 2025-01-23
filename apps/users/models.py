from django.db import models
from apps.general.models import BaseModel

# Модель пользователя
class User(BaseModel):
    user_id = models.BigIntegerField(unique=True, null=True, verbose_name="ID пользователя")
    full_name = models.CharField(max_length=255, null=True, verbose_name="Полное имя")
    username = models.CharField(max_length=255, null=True, blank=True, unique=True, verbose_name="Имя пользователя")
    is_logined = models.BooleanField(default=False, verbose_name="Вошли в систему?")
    account = models.ForeignKey("users.Account", on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.full_name} ({self.username})" if self.full_name else f"Пользователь {self.user_id}"


class Account(BaseModel):
    phone_number = models.CharField(max_length=255, null=True, blank=True, unique=True, verbose_name="Номер телефона")
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name="Электронная почта")
    is_admin = models.BooleanField(default=False, verbose_name="Администратор?")
    balance_usd = models.DecimalField(
        null=True, blank=True, default=0, verbose_name="Баланс (USD)", max_digits=12, decimal_places=2)
    balance_uzs = models.DecimalField(
        null=True, blank=True, default=0, verbose_name="Баланс (UZS)", max_digits=12, decimal_places=2)
    is_banned = models.BooleanField(default=False, verbose_name="Заблокирован?")
    password = models.CharField(max_length=255, verbose_name="Password")
    
    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"
    
    def __str__(self):
        return f"{self.phone_number} ({self.email})" if self.phone_number else f"Аккаунт {self.pk}"

# Модель администратора
class Admin(BaseModel):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, verbose_name="Аккаунт")

    class Meta:
        verbose_name = "Администратор"
        verbose_name_plural = "Администраторы"

    def save(self, *args, **kwargs):
        self.account.is_admin = True
        self.account.save()

        return super().save(*args, **kwargs)
    
    def delete(self, using = ..., keep_parents = ...):
        self.account.is_admin = False
        self.account.save()

        return super().delete(using, keep_parents)

    def __str__(self):
        return f"Администратор - {self.user.full_name}"
