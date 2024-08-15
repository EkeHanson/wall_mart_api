# recharge/views.py

from rest_framework import viewsets, permissions
from .models import Recharge
from .serializers import RechargeSerializer
from rest_framework import viewsets, status, views
from rest_framework.response import Response

# class RechargeViewSet(viewsets.ModelViewSet):
#     queryset = Recharge.objects.all()
#     serializer_class = RechargeSerializer
#     permission_classes = [permissions.AllowAny]  # Allows access to anyone

#     def perform_create(self, serializer):
#         # If the user is authenticated, associate the recharge with the user
#         # Otherwise, handle the case where the user is not provided (optional)
#         if self.request.user.is_authenticated:
#             serializer.save(user=self.request.user)
#         else:
#             serializer.save()  # Save without associating a user
from rest_framework.exceptions import ValidationError

class RechargeViewSet(viewsets.ModelViewSet):
    queryset = Recharge.objects.all()
    serializer_class = RechargeSerializer
    permission_classes = [permissions.AllowAny]  # Allows access to anyone

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        try:

            if not serializer.is_valid():
                print(f"CREATE request errors: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # If the user is authenticated, associate the recharge with the user
            # if self.request.user.is_authenticated:
            #     serializer.save(user=self.request.user)
            else:
                serializer.save()  # Save without associating a user
        except ValidationError as e:
            # Raise a custom error message
            raise ValidationError({"error": "There was an issue creating the recharge. Please check your input and try again.", "details": str(e)})
