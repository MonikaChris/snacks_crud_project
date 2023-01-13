from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class MyAccountManager(BaseUserManager):
    def create_superuser(self, email, username, password, **other_fields):
        other_fields.setdefault('is_active', True)
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)

        if not username:
            raise ValueError("User must have a username")

        if other_fields.get('is_active') is not True:
            raise ValueError("is_active must be assigned to True")

        if other_fields.get('is_staff') is not True:
            raise ValueError("is_staff must be assigned to True")

        if other_fields.get('is_superuser') is not True:
            raise ValueError("is_superuser must be assigned to True")

        user = self.create_user(email, username, password, **other_fields)
        user.save()
        return user

    def create_user(self, email, username, password, **other_fields):
        if not email:
            raise ValueError("User must have an email address")
        email = self.normalize_email(email)

        if not username:
            raise ValueError("User must have a username")

        user = self.model(email=email, username=username, **other_fields)
        user.set_password(password)
        user.save()
        return user


class Account(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    about = models.TextField(max_length=500, blank=True)
    last_name = models.TextField(max_length=30, blank=True)
    first_name = models.TextField(max_length=30, blank=True)

    # Required fields
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyAccountManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
