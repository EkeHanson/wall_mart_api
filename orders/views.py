from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from decimal import Decimal
from .models import OrderGrabbing, CustomUser
from .serializers import  OrderGrabbingSerializer

# class OrderViewSet(viewsets.ModelViewSet):
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = [AllowAny]

class OrderGrabbingViewSet(viewsets.ModelViewSet):
    queryset = OrderGrabbing.objects.all()
    serializer_class = OrderGrabbingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user

        original_balance = Decimal( user.balance) 
        if user.level == "VIP1":
            grab_amount = Decimal(10)
            if user.balance < grab_amount - 1:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

            if user.grabbed_orders_count >= 3:
                return Response({"error": "Grab limit reached"}, status=status.HTTP_400_BAD_REQUEST)

            user.balance = original_balance - grab_amount
    
            user.grabbed_orders_count + 1

            # Calculate commission (20% of order price)

            commission_amount = Decimal(2)  # Ensure commission_amount is a Decimal
            today = timezone.now().date()  # Get today's date

            # Check the last order grabbing day
            last_grab_day = None
            if user.ordergrabbing_set.exists():
                last_grab_day = user.ordergrabbing_set.latest('grabbed_at').grabbed_at.date()

            # Update user's commission based on the day
            if last_grab_day is None or last_grab_day == today:
                user.commission2 += commission_amount
            else:
                user.commission1 += commission_amount
            user.save()

            # Create order grabbing record
            grabbing = OrderGrabbing.objects.create(user=user, commission=commission_amount, grabbed_at=timezone.now())
            serializer = self.get_serializer(grabbing)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif user.level == "VIP2":
            grab_amount = Decimal(20)
            if user.balance < grab_amount - 1:
                return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

            if user.grabbed_orders_count >= 2:
                return Response({"error": "Grab limit reached"}, status=status.HTTP_400_BAD_REQUEST)
            
            if user.grabbed_orders_count < 1:
                user.balance = original_balance - Decimal(40) 
            elif user.grabbed_orders_count >= 1:
                user.balance = original_balance - grab_amount
    
            user.grabbed_orders_count + 1

            # Calculate commission (20% of order price)

            commission_amount = Decimal(9)  # Ensure commission_amount is a Decimal
            today = timezone.now().date()  # Get today's date

            # Check the last order grabbing day
            last_grab_day = None
            if user.ordergrabbing_set.exists():
                last_grab_day = user.ordergrabbing_set.latest('grabbed_at').grabbed_at.date()

            # Update user's commission based on the day
            if last_grab_day is None or last_grab_day == today:
                user.commission2 += commission_amount
            else:
                user.commission1 += commission_amount
            user.save()

            # Create order grabbing record
            grabbing = OrderGrabbing.objects.create(user=user, commission=commission_amount, grabbed_at=timezone.now())
            serializer = self.get_serializer(grabbing)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # elif user.level == "VIP3":
        #     grab_amount = Decimal(20)
        #     if user.balance < grab_amount - 1:
        #         return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

        #     if user.grabbed_orders_count >= 12:
        #         return Response({"error": "Grab limit reached"}, status=status.HTTP_400_BAD_REQUEST)
            
        #     if user.grabbed_orders_count < 1:
        #         user.balance = original_balance - Decimal(70) 
        #     elif user.grabbed_orders_count >= 1:
        #         user.balance = original_balance - Decimal(120)
        #     elif user.grabbed_orders_count >= 2:
        #         user.balance = original_balance - Decimal(200)
        #     elif user.grabbed_orders_count >= 3:
        #         user.balance = original_balance - Decimal(500)
        #     elif user.grabbed_orders_count >= 4:
        #         user.balance = original_balance - Decimal(900)
        #     elif user.grabbed_orders_count >= 5:
        #         user.balance = original_balance - Decimal(1200)
        #     elif user.grabbed_orders_count >= 6:
        #         user.balance = original_balance - Decimal(1500)
        #     elif user.grabbed_orders_count >= 7:
        #         user.balance = original_balance - Decimal(2200)
        #     elif user.grabbed_orders_count >= 8:
        #         user.balance = original_balance - Decimal(3000)
        #     elif user.grabbed_orders_count >= 9:
        #         user.balance = original_balance - Decimal(3500)
        #     elif user.grabbed_orders_count >= 10:
        #         user.balance = original_balance - Decimal(3950)
        #     elif user.grabbed_orders_count >= 11:
        #         user.balance = original_balance - Decimal(4200)
    
    
        #     user.grabbed_orders_count + 1

        #     # Calculate commission (20% of order price)

        #     commission_amount = Decimal(9)  # Ensure commission_amount is a Decimal
        #     today = timezone.now().date()  # Get today's date

        #     # Check the last order grabbing day
        #     last_grab_day = None
        #     if user.ordergrabbing_set.exists():
        #         last_grab_day = user.ordergrabbing_set.latest('grabbed_at').grabbed_at.date()

        #     # Update user's commission based on the day
        #     if last_grab_day is None or last_grab_day == today:
        #         user.commission2 += commission_amount
        #     else:
        #         user.commission1 += commission_amount
        #     user.save()

        #     # Create order grabbing record
        #     grabbing = OrderGrabbing.objects.create(user=user, commission=commission_amount, grabbed_at=timezone.now())
        #     serializer = self.get_serializer(grabbing)

        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
