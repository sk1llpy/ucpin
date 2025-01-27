from django.db import models

# Create your choices here.
class BalanceTypeChoices(models.TextChoices):
    usd = ("usd", "USD")
    uzs = ("uzs", "UZS")

class PaymentTypeChoices(models.TextChoices):
    # USD
    tolov1 = ("tolov 1", "tolov 1 (usd)")
    tolov2 = ("tolov 2", "tolov 2 (usd)")
    tolov3 = ("tolov 3", "tolov 3 (usd)")

    # UZS
    tolov1 = ("tolov 1", "tolov 1 (uzs)")
    tolov2 = ("tolov 2", "tolov 2 (uzs)")
    tolov3 = ("tolov 3", "tolov 3 (uzs)")