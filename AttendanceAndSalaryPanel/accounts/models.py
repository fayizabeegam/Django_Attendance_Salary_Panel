from django.db import models
from attendance.models import*
from .managers import CustomUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
# Create your models here.

class User(AbstractBaseUser,PermissionsMixin):
    ROLE_CHOICES = [
        ('Admin','Admin'),
        ('HR','HR'),
        ('Employee','Employee')
    ]

    ACTIVE = 0
    INACTIVE = 1
    STATUS_CHOICES = (
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
    )
    
    IFID = models.CharField(max_length=20, unique=True, blank=True, null=True)
    username = models.CharField(max_length=150, unique=True)
    mobile = models.CharField(max_length=10, unique=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=0)


    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['mobile']

    def has_perm(self, perm, obj=None):
        # Handle global permissions here
        return self.is_staff

    def has_module_perms(self, app_label):
        # Handle app-specific permissions here
        return self.is_staff

    def __str__(self):
        return f"{self.username}"