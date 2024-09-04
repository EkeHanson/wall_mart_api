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
from rest_framework.decorators import action


from django.contrib.auth import authenticate
from rest_framework import views, status
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from .serializers import PasswordResetSerializer

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta
#from twilio.rest import Client  # Assuming Twilio for SMS

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
    queryset = CustomUser.objects.all().order_by('-id')  # LIFO principle
    serializer_class = CustomUserSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if not serializer.is_valid():
            # Log the specific errors for debugging
            print(f"PATCH request errors: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(serializer.data)

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

    @action(detail=False, methods=['get'], url_path='by-level/(?P<level>[^/.]+)')
    def get_users_by_level(self, request, level=None):
        if level not in ['VIP1', 'VIP2', 'VIP3']:
            return Response({"error": "Invalid level"}, status=status.HTTP_400_BAD_REQUEST)
        
        users = CustomUser.objects.filter(level=level).order_by('-id')  # LIFO principle
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
            'user_invitation_code': invitation_code_serializer.data,
            'firstName': user.firstName,
            'phone': user.phone,
            'user_type': user.user_type,
            'lastName': user.lastName
        }
        return Response(context, status=status.HTTP_200_OK)


class ResetPasswordView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')

        if not phone:
            return Response({'error': 'Phone is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(phone=phone)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this Phone number does not exist'}, status=status.HTTP_404_NOT_FOUND)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_link = f"{uid}/{token}/"

    
        context = {
            "code" : reset_link
        }

        return Response(context, status=status.HTTP_200_OK)



class PasswordResetConfirmView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            serializer = PasswordResetSerializer(data=request.data)

            if serializer.is_valid():
                new_password = serializer.validated_data.get("new_password")
                user.set_password(new_password)
                user.save()

                if not user.is_active:
                    user.is_active = True
                    user.save()

                return Response({'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Invalid token or user ID'}, status=status.HTTP_400_BAD_REQUEST)
