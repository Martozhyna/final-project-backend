from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.users.managers import UserManager


class UserModel(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'auth_user'
        ordering = ('-id',)

    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=25)

    USERNAME_FIELD = 'email'

    objects = UserManager()

