from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser


class InvitationCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code
    
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, user_type, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, user_type, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser has to have is_staff being True")
        
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser has to have is_superuser being True")
        
        return self.create_user(email=email, password=password, user_type=user_type, **extra_fields)


class CustomUser(AbstractUser):
    LEVEL_CHOICES = [
    ('VIP1', 'VIP1'),
    ('VIP2', 'VIP2'),
    ('VIP3', 'VIP3'),
    ]
    
    level = models.CharField(max_length=5, choices=LEVEL_CHOICES)
    reset_token = models.CharField(max_length=100, blank=True, null=True)
    reset_token_expires = models.DateTimeField(null=True, blank=True)

    phone = models.CharField(max_length=15, unique=True)

    balance = models.DecimalField(max_digits=10, decimal_places=1, default=0.0)
    unsettle = models.DecimalField(max_digits=10, decimal_places=1, default=0.0)

    commission1 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    commission2 = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    withdrawalPassword = models.CharField(max_length=255)  # Removed min_length

    grabbed_orders_count = models.PositiveIntegerField(default=0)

    firstName = models.CharField(max_length=255, null=True, blank=True)
    lastName = models.CharField(max_length=255, null=True, blank=True)
    middleName = models.CharField(max_length=255, default="None")

    country = models.CharField(max_length=255, null=True, blank=True)

    username = models.CharField(max_length=80, unique=False, blank=True, null=True)
    email = models.EmailField(max_length=80,  null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=[('admin', 'Admin'), ('client', 'Client')])

    invitationCode = models.ForeignKey(InvitationCode, on_delete=models.SET_NULL, null=True, blank=True)
    created_ip = models.GenericIPAddressField(null=True, blank=True)
    
    objects = CustomUserManager()
    USERNAME_FIELD = "phone"  # Set the email field as the unique identifier
    REQUIRED_FIELDS = ["user_type"]

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
