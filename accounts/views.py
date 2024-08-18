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
            'lastName': user.lastName
        }
        return Response(context, status=status.HTTP_200_OK)



# class PasswordResetRequestView(views.APIView):
#     def post(self, request):
#         phone = request.data.get('phone')

#         if not phone:
#             return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = CustomUser.objects.get(phone=phone)
#         except CustomUser.DoesNotExist:
#             return Response({'error': 'User with this phone number does not exist'}, status=status.HTTP_404_NOT_FOUND)

#         # Generate reset token
#         reset_token = get_random_string(length=32)
#         reset_token_expires = timezone.now() + timedelta(hours=1)  # Token valid for 1 hour

#         user.reset_token = reset_token
#         user.reset_token_expires = reset_token_expires
#         user.save()

#         # Send SMS with Twilio
#         try:
#             #client = Client('TWILIO_ACCOUNT_SID', 'TWILIO_AUTH_TOKEN')
#             client = Client('https://v3.api.termii.com', 'TLcylVFKgAvGdeNAMOzbjyrizSWnadGjdxFblqXHOTaBGkUNhXECmHKBiIXZUo')
#             client.messages.create(
#                 body=f"Your password reset token is: {reset_token}",
#                 from_='+1234567890',  # Your Twilio phone number
#                 to=phone
#             )
#             return Response({'message': 'Reset token sent via SMS'}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': 'Failed to send SMS'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class PasswordResetConfirmView(views.APIView):
#     def post(self, request):
#         phone = request.data.get('phone')
#         reset_token = request.data.get('reset_token')
#         new_password = request.data.get('new_password')

#         if not phone or not reset_token or not new_password:
#             return Response({'error': 'Phone number, reset token, and new password are required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = CustomUser.objects.get(phone=phone, reset_token=reset_token)
#         except CustomUser.DoesNotExist:
#             return Response({'error': 'Invalid phone number or reset token'}, status=status.HTTP_400_BAD_REQUEST)

#         if user.reset_token_expires < timezone.now():
#             return Response({'error': 'Reset token has expired'}, status=status.HTTP_400_BAD_REQUEST)

#         user.set_password(new_password)
#         user.reset_token = None
#         user.reset_token_expires = None
#         user.save()

#         return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)
