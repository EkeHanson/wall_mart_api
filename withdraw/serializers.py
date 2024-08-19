from rest_framework import serializers
from .models import Withdraw
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum

class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = '__all__'

    # def validate(self, data):
    #     user = self.context['request'].user  # Get the user from the request context
    #     amount = data.get('amount')  # Correct field name from the model

      
        
    #     # Calculate the total withdrawn amount by the user for the day
    #     today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    #     today_end = today_start + timedelta(days=1)

    #     total_withdrawn_today = Withdraw.objects.filter(user=user, created_at__range=(today_start, today_end)).aggregate(
    #         total_withdrawn=Sum('amount')
    #     )['total_withdrawn'] or 0

    #     # Add more logic if you have withdrawal limits (e.g., max daily withdrawal limit)
    #     max_daily_limit = 5000.00  # Example daily limit
    #     if total_withdrawn_today + amount > max_daily_limit:
    #         raise serializers.ValidationError("You have exceeded your daily withdrawal limit.")
        
    #     return data
