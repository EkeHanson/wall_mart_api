from rest_framework import serializers
from .models import Order, OrderGrabbing

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class OrderGrabbingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderGrabbing
        fields = '__all__'

