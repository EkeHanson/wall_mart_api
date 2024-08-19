from rest_framework import serializers
from .models import Recharge

class RechargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recharge
        fields = "__all__"
        read_only_fields = ['payment_id', 'user_balance', 'created_at']
    
    def validate_amount_top_up(self, value):
        if value <= 0:
            raise serializers.ValidationError("The amount to top up must be greater than zero.")
        return value

    def validate_receipt_image(self, value):
        if value.size > 5 * 1024 * 1024:  # 5MB limit
            raise serializers.ValidationError("The receipt image file size should not exceed 5MB.")
        return value
