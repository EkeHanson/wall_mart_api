# In the orders/models.py

from django.db import models
from accounts.models import CustomUser

# class Order(models.Model):
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Order {self.id} by {self.user.phone}"

class OrderGrabbing(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    grabbed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone} grabbed Order {self.order.id}"

    def save(self, *args, **kwargs):
        # Check if the user has enough balance
        # if self.user.balance < self.order.price:
        #     raise ValueError("Insufficient balance to grab the order.")
        
        # Check if the user has already grabbed 3 orders
        # if self.user.grabbed_orders_count >= 3:
        #     #raise ValueError("User has already grabbed 3 orders.")
        #     return "User has already grabbed 3 orders."
          
        # Deduct the price of the order from the user's balance
        # self.user.balance -= self.order.price
        # self.user.unsettle += commision
        self.user.grabbed_orders_count += 1
        self.user.save()

        super().save(*args, **kwargs)


