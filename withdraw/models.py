import uuid
from django.db import models
from django.conf import settings


class Withdraw(models.Model):
    RECHARGE_METHOD_CHOICES = [
        ('bank', 'Bank Transfer'),
        ('crypto', 'Cryptocurrency'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='withdraws')
    bankAccountNumber = models.CharField(max_length=255)
    bankName = models.CharField(max_length=50)
    phoneNumber = models.CharField(max_length=15)
    selectedMethod = models.CharField(max_length=20, choices=RECHARGE_METHOD_CHOICES)
    user_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    user_firstName = models.CharField(max_length=100, default="Hanson")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)  # New field added

    def save(self, *args, **kwargs):
        # Set the user_balance to the user's current balance before saving
        self.user_balance = self.user.unsettle
        self.user_firstName = self.user.firstName
        super(Withdraw, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.phone} - {self.amount}"
