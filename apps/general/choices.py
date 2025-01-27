from django.db import models

# Create your choices here.
class BalanceTypeChoices(models.TextChoices):
    usd = ("usd", "USD")
    uzs = ("uzs", "UZS")

class PaymentTypeChoices(models.TextChoices):
    # USD
    binance = ("binance", "Binance Pay")
    trc = ("trc", "TRC20")
    bep = ("bep", "BEP20")
    bybit = ("bybit", "Bybit")

    # UZS
    uzcard = ("uzacrd", "UzCard")
    humo = ("humo", "HUMO Card")