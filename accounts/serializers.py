from rest_framework import serializers
from .models import CustomUser, InvitationCode

class CustomUserSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(default='client')
    class Meta:
        model = CustomUser
        fields = '__all__'

class InvitationCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationCode
        fields = '__all__'
