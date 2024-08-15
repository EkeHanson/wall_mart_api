from django.contrib import admin
from .models import Recharge

@admin.register(Recharge)
class RechargeAdmin(admin.ModelAdmin):
    list_display = ('user', 'recharge_method', 'payment_id', 'amount_top_up', 'created_at')
    search_fields = ('user__phone', 'payment_id')
    list_filter = ('recharge_method', 'created_at')