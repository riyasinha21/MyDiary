
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .manager import CustomUserManager
from django.utils import timezone
from datetime import timedelta
from .choices import COUNTRY_CODE_CHOICES


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        

def profile_image_upload_path(instance, filename):
    user_name = "_".join(instance.name.split()).lower()

    return f"profile/{instance.id}_{user_name}/{filename}"

class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    
    country_code = models.CharField(
        max_length=5,
        choices=COUNTRY_CODE_CHOICES
    )
    
    phone_number = models.CharField(max_length=15,unique=True)
    
    profile_image = models.ImageField(
        upload_to=profile_image_upload_path,
        blank=True,
        null=True
    )
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True,null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name","phone_number"]
    
    def __str__(self):
        return self.email

    
class PendingRegistration(BaseModel):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    
    country_code = models.CharField(
        max_length=5,
        choices=COUNTRY_CODE_CHOICES
    )
    
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    otp = models.CharField(max_length=6)
    
    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=15)

    
    def __str__(self):
        return f"Pending registration for {self.email}"
    
class PrivacySettings(BaseModel):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="privacy_settings"
    )

    profile_visibility = models.CharField(
        max_length=10,
        choices=[
            ("public", "Public"),
            ("friends", "Friends Only"),
            ("private", "Private"),
        ],
        default="public"
    )

    friend_request_permission = models.CharField(
        max_length=10,
        choices=[
            ("everyone", "Everyone"),
            ("friends", "Friends of Friends"),
            ("nobody", "Nobody"),
        ],
        default="everyone"
    )

    searchable = models.BooleanField(
        default=True
    )

    def __str__(self):
        return f"Privacy settings for {self.user.email}"