from django.db import models

# Create your choices here.
class BalanceTypeChoices(models.TextChoices):
    usd = ("usd", "USD")
    uzs = ("uzs", "UZS")