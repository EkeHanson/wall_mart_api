from django.db import models
from accounts.models import CustomUser
from datetime import datetime, timedelta

class Order(models.Model):

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.phone}"

class OrderGrabbing(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    grabbed_at = models.DateTimeField(auto_now_add=True)


    # def grab_order(self, order_cost):
    #     if self.orders_grabbed < 3:
    #         if self.balance >= order_cost:
    #             self.balance -= order_cost
    #             self.orders_grabbed += 1
    #             self.last_order_grabbed = datetime.now()
    #             self.save()
    #             return True
    #         else:
    #             raise ValueError("Insufficient balance")
    #     else:
    #         raise ValueError("Order limit reached for this level")

    # def reset_orders(self):
    #     if self.last_order_grabbed:
    #         if datetime.now() >= self.last_order_grabbed + timedelta(days=1):
    #             self.orders_grabbed = 0
    #             self.save()


    def __str__(self):
        return f"{self.user.phone} grabbed Order {self.order.id}"


