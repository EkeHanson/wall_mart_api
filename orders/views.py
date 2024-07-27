from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from .models import Order, OrderGrabbing, CustomUser
from .serializers import OrderSerializer, OrderGrabbingSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]

class OrderGrabbingViewSet(viewsets.ModelViewSet):
    queryset = OrderGrabbing.objects.all()
    serializer_class = OrderGrabbingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        order_id = request.data.get('order')

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({"error": "Order not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if user has enough balance and has not exceeded the grab limit
        if user.balance < order.price:
            return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

        if OrderGrabbing.objects.filter(user=user).count() >= 3:
            return Response({"error": "Grab limit reached"}, status=status.HTTP_400_BAD_REQUEST)

        # Subtract price from user balance and add a commission
        user.balance -= order.price
        user.grabbed_orders_count += 1
        user.save()

        # Calculate commission (2% of order price)
        #commission_amount = order.price * 0.02
        commission_amount = 2.00
        today = timezone.now().strftime("%Y-%m-%d")
        last_grab_day = None

        # Check the last order grabbing day
        if user.ordergrabbing_set.exists():
            last_grab_day = user.ordergrabbing_set.latest('created_at').day

        # Create order grabbing record
        grabbing = OrderGrabbing.objects.create(user=user, order=order, commission=commission_amount, grabbed_at=today)
        serializer = self.get_serializer(grabbing)

        # Update user's commission based on the day
        if last_grab_day is None or last_grab_day == today:
            user.commission2 = commission_amount
        else:
            user.commission1 = commission_amount
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
