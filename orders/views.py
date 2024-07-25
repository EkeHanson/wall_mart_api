from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderGrabbing
from .serializers import OrderSerializer, OrderGrabbingSerializer
from accounts.models import CustomUser

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

class OrderGrabbingViewSet(viewsets.ModelViewSet):
    queryset = OrderGrabbing.objects.all()
    serializer_class = OrderGrabbingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        order_id = request.data.get('order_id')
        order = Order.objects.get(id=order_id)

        # Check if user has enough balance and has not exceeded the grab limit
        if user.balance < order.price:
            return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

        if OrderGrabbing.objects.filter(user=user).count() >= 3:
            return Response({"error": "Grab limit reached"}, status=status.HTTP_400_BAD_REQUEST)

        # Subtract price from user balance
        user.balance -= order.price
        user.save()

        # Create order grabbing record
        grabbing = OrderGrabbing.objects.create(user=user, order=order)
        serializer = self.get_serializer(grabbing)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
