from rest_framework import viewsets, permissions, status
from .models import Withdraw
from .serializers import WithdrawSerializer
from rest_framework.response import Response

class WithdrawViewSet(viewsets.ModelViewSet):
    # Order the queryset in descending order by 'id' or 'created_at' for LIFO behavior
    queryset = Withdraw.objects.all().order_by('-created_at')  # Change '-id' to '-created_at' if needed
    serializer_class = WithdrawSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # This will call the validate method in the serializer
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
