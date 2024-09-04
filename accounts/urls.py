from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomUserViewSet, InvitationCodeViewSet, LoginView
from .views import ResetPasswordView, PasswordResetConfirmView

router = DefaultRouter()
router.register(r'users', CustomUserViewSet)
router.register(r'invitation-codes', InvitationCodeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),

    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='reset-password-confirm'),
]
