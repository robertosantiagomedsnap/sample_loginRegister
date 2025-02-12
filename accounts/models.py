from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    # Determine user type: Personal or Company
    user_type = models.CharField(max_length=10, choices=[('personal', 'Personal'), ('company', 'Company')], default='personal')

    # Fields for personal users
    employee_specialty = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('general', 'General'),
        ('aesthetic_medicine', 'Aesthetic Medicine'),
        ('dermatologist', 'Dermatologist'),
        ('plastic_surgery', 'Plastic Surgery'),
        ('dermatology', 'Dermatology'),
    ])
    gender = models.CharField(max_length=10, choices=[('male', 'Male'), ('female', 'Female')], blank=True, null=True)

    # Fields for company users
    company_name = models.CharField(max_length=255, blank=True, null=True)
    num_employees = models.IntegerField(blank=True, null=True)
    vat_number = models.CharField(max_length=50, blank=True, null=True)
    company_phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
