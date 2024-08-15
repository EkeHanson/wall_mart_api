from rest_framework import serializers
from .models import BankDetail, CryptoWalletDetail

class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = "__all__"

class CryptoWalletDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CryptoWalletDetail
        fields = ['id', 'wallet_type', 'wallet_address']
