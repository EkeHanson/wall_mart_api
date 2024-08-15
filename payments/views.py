from rest_framework import viewsets, permissions
from .models import BankDetail, CryptoWalletDetail
from .serializers import BankDetailSerializer, CryptoWalletDetailSerializer

class BankDetailViewSet(viewsets.ModelViewSet):
    queryset = BankDetail.objects.all()
    serializer_class = BankDetailSerializer
    permission_classes = [permissions.AllowAny]  # Allows access to anyone

class CryptoWalletDetailViewSet(viewsets.ModelViewSet):
    queryset = CryptoWalletDetail.objects.all()
    serializer_class = CryptoWalletDetailSerializer
    permission_classes = [permissions.AllowAny]  # Allows access to anyone
