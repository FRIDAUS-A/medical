from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import re
import uuid


def validate_phone_number(value):
    if not re.match(r'^\+?[1-9]\d{1,14}$', value):
        raise ValidationError('Invalid phone number format.')



class User(AbstractBaseUser, PermissionsMixin):
    # Common fields for all users
    id = models.CharField(max_length=50, primary_key=True, blank=False,  default=uuid.uuid4())
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, validators=[validate_phone_number])
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    password = models.CharField(max_length=50, blank=False)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(
        max_length=10,
        choices=[
            ('patient', 'Patient'),
            ('doctor', 'Doctor'),
            ('admin', 'Admin')
        ],
        default='patient'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Patient-specific fields
    medical_history = models.TextField(blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    emergency_contact_relationship = models.CharField(max_length=50, blank=True, null=True)

    # Doctor-specific fields
    specialization = models.CharField(max_length=100, blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    availability = models.JSONField(blank=True, null=True)  # Example: [{"day": "Monday", "slots": ["09:00-12:00"]}]
    USERNAME_FIELD = 'email'
    objects = CustomUserManager()

    def __str__(self):
        return self.email
