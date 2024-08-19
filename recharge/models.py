# recharge/models.py

import uuid
from django.db import models
from django.conf import settings

class Recharge(models.Model):
    RECHARGE_METHOD_CHOICES = [
        ('bank_transfer', 'Bank Transfer'),
        ('credit_card', 'Credit Card'),
        ('mobile_payment', 'Mobile Payment'),
        ('crypto', 'Cryptocurrency'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recharges')
    payment_name = models.CharField(max_length=255)
    recharge_method = models.CharField(max_length=20, choices=RECHARGE_METHOD_CHOICES)
    payment_id = models.CharField(max_length=100, unique=True, editable=False)
    user_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    user_firstName= models.CharField(max_length=100,  default="Hanson")
    amount_top_up = models.DecimalField(max_digits=10, decimal_places=2)
    # receipt_image = models.ImageField(upload_to='receipts/')

    is_approved = models.BooleanField(default=False)  # New field ad
    
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Generate a unique payment_id if it doesn't already exist
        if not self.payment_id:
            self.payment_id = str(uuid.uuid4())[:12].replace("-", "").upper()
        
        # Set the user_balance to the user's current balance before saving
        self.user_balance = self.user.balance
        self.user_firstName= self.user.firstName
        
        super(Recharge, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.phone} - {self.amount_top_up} - {self.payment_id}"
