from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    AUTHOR = 'AUTHOR'
    REVIEWER = 'REVIEWER'
    ANALYST = 'ANALYST'
    CUSTOMER = 'CUSTOMER'

    ROLE = ((AUTHOR, 'Author'),
            (REVIEWER, 'Reviewer'),
            (ANALYST, 'Analyst'),
            (CUSTOMER, 'Customer'))

    username = None
    name = models.CharField(max_length=50, db_index=True)
    email = models.EmailField(unique=True, db_index=True)
    role = models.CharField(choices=ROLE, max_length=20, db_index=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.name
