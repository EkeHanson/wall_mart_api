# recharge/serializers.py

from rest_framework import serializers
from .models import Recharge

class RechargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recharge
        fields = '__all__'
        read_only_fields = ['payment_id', 'user_balance', 'created_at']
