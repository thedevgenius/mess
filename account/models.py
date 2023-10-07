from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise AssertionError('Phone must be set')
    
        phone = self.normalize_email(phone)
        user = self.model(phone = phone, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user
    

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(phone, password, **extra_fields)
    
class Member(AbstractUser):
    username = None
    phone = models.CharField(unique=True, max_length=15)
    profile_image = models.ImageField(upload_to='user/', null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.first_name
    
    def __lt__(self, other):
        # Define how you want to compare two Member instances
        # For example, you could compare them based on a specific field like 'name'
        return self.first_name < other.name
    