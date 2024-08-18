from django.db import models
from django.core.exceptions import ValidationError

class BankDetail(models.Model):
    bank_name = models.CharField(max_length=100, default="Banco Prepago Tenpo")
    account_number = models.CharField(max_length=20, default= "111119469406")
    recipient_name = models.CharField(max_length=100, default= "Gonsalo Osvaldo Cornejo Rivero")
    ruth = models.CharField(max_length=15, default=1946406-7)

    def __str__(self):
        return f"{self.recipient_name} - {self.bank_name}"

    def save(self, *args, **kwargs):
        # Check if any instance of BankDetail already exists
        if BankDetail.objects.exists() and not self.pk:
            raise ValidationError("Only one BankDetail instance is allowed.")
        return super(BankDetail, self).save(*args, **kwargs)

class CryptoWalletDetail(models.Model):
    WALLET_TYPES = [
        ('USDT', 'USDT'),
        ('BINANCE', 'Binance'),
        ('TON', 'TON'),
        ('BTC', 'Bitcoin'),
        ('TRX', 'TRON'),
        ('TRC20', 'TRC20'),
    ]

    wallet_type = models.CharField(max_length=20, choices=WALLET_TYPES, unique=True)
    wallet_address = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.wallet_type} - {self.wallet_address}"
