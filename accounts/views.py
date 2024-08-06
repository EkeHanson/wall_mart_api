from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import CustomUser, InvitationCode
from .serializers import CustomUserSerializer, InvitationCodeSerializer
import uuid
import hashlib
import logging
from rest_framework.views import APIView

logger = logging.getLogger(__name__)


def generate_short_code():
    return hashlib.md5(uuid.uuid4().bytes).hexdigest()[:10]  # 10-character hash


class InvitationCodeViewSet(viewsets.ModelViewSet):
    queryset = InvitationCode.objects.all()
    serializer_class = InvitationCodeSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        code = generate_short_code()  # Use the new method to generate a shorter code
        invitationCode = InvitationCode.objects.create(code=code)
        serializer = self.get_serializer(invitationCode)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class CustomUserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        invitationCode = request.data.get('invitationCode')
        if not invitationCode:
            logger.error("Invitation code is required")
            return Response({"error": "Invitation code is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            code_instance = InvitationCode.objects.get(code=invitationCode, is_used=False)
        except InvitationCode.DoesNotExist:
            logger.error("Invalid or already used invitation code")
            return Response({"error": "Invalid or already used invitation code"}, status=status.HTTP_400_BAD_REQUEST)

        # Get the IP address from the request
        user_ip = request.META.get('REMOTE_ADDR')

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        user.balance += 10
        user.created_ip = user_ip  # Save the IP address
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')

        if phone is None or password is None:
            return Response({'error': 'Please provide both phone and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=phone, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        
        # Serialize the invitation code
        invitation_code_serializer = InvitationCodeSerializer(user.invitationCode)
        
        context = {
            'token': token.key,
            'user_id': user.id,
            'user_invitation_code': invitation_code_serializer.data
        }
        return Response(context, status=status.HTTP_200_OK)
