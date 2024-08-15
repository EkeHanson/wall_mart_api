from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Recharge
from .serializers import RechargeSerializer


class RechargeViewSet(viewsets.ModelViewSet):
    queryset = Recharge.objects.all().order_by('-created_at')  # Ordering by created_at descending
    serializer_class = RechargeSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            # Return detailed error message
            error_details = serializer.errors
            return Response({"errors": error_details}, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        else:
            # Return detailed error message
            error_details = serializer.errors
            return Response({"errors": error_details}, status=status.HTTP_400_BAD_REQUEST)
