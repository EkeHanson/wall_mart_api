from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import CustomUser, InvitationCode
from .serializers import CustomUserSerializer, InvitationCodeSerializer
import uuid
import logging
from rest_framework.views import APIView

logger = logging.getLogger(__name__)

class InvitationCodeViewSet(viewsets.ModelViewSet):
    queryset = InvitationCode.objects.all()
    serializer_class = InvitationCodeSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        code = str(uuid.uuid4())
        invitationCode = InvitationCode.objects.create(code=code)
        serializer = self.get_serializer(invitationCode)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# class CustomUserViewSet(viewsets.ModelViewSet):
#     permission_classes = [AllowAny]
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer

#     def create(self, request, *args, **kwargs):
#         invitationCode = request.data.get('invitationCode')
#         if not invitationCode:
#             return Response({"error": "Invitation code is required"}, status=status.HTTP_400_BAD_REQUEST)
        
#         try:
#             code_instance = InvitationCode.objects.get(code=invitationCode, is_used=False)
#         except InvitationCode.DoesNotExist:
#             return Response({"error": "Invalid or already used invitation code"}, status=status.HTTP_400_BAD_REQUEST)

#         response = super().create(request, *args, **kwargs)
#         code_instance.is_used = True
#         code_instance.save()
#         return response


class CustomUserViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def create(self, request, *args, **kwargs):
        invitationCode = request.data.get('invitationCode')
        if not invitationCode:
            return Response({"error": "Invitation code is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            code_instance = InvitationCode.objects.get(code=invitationCode, is_used=False)
        except InvitationCode.DoesNotExist:
            return Response({"error": "Invalid or already used invitation code"}, status=status.HTTP_400_BAD_REQUEST)

        response = super().create(request, *args, **kwargs)

        # Increase balance by 10 after successful user creation
        user = CustomUser.objects.get(id=response.data['id'])
        user.balance += 10
        user.save()

        code_instance.is_used = True
        code_instance.save()
        return response

        

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get('phone')
        password = request.data.get('password')

        if phone is None or password is None:
            logger.error('Phone or password not provided')
            return Response({'error': 'Please provide both phone and password'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=phone, password=password)

        if not user:
            logger.error(f'Invalid credentials for phone: {phone}')
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        logger.info(f'User {user.id} authenticated successfully')
        context = {'token': token.key,
                   "user_id" : user.id
                   }
        return Response(context, status=status.HTTP_200_OK)

