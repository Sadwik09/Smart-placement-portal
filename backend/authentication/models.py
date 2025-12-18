from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
import secrets


class User(AbstractUser):
    """Custom User model with role-based access"""
    
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('recruiter', 'Recruiter'),
        ('admin', 'Admin'),
    )
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_approved = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']
    
    def __str__(self):
        return f"{self.email} ({self.role})"
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class EmailVerificationToken(models.Model):
    """Stores email verification tokens for users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='email_tokens')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    @staticmethod
    def create_for_user(user, ttl_hours: int = 24):
        token = secrets.token_urlsafe(32)
        return EmailVerificationToken.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timezone.timedelta(hours=ttl_hours)
        )

    def is_valid(self):
        return not self.used and timezone.now() < self.expires_at


class PasswordResetToken(models.Model):
    """Stores password reset tokens for users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    @staticmethod
    def create_for_user(user, ttl_hours: int = 2):
        token = secrets.token_urlsafe(32)
        return PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timezone.timedelta(hours=ttl_hours)
        )

    def is_valid(self):
        return not self.used and timezone.now() < self.expires_at
