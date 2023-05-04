from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that replaces the username field with an email field.

    This model also includes fields for tracking whether the user
    is staff or active, and when they joined. It uses a custom
    manager for querying and creating users.

    Attributes:
        - email: A unique EmailField representing the user's email address.
        - is_staff: A boolean field indicating whether the user
        is a staff member.
        - is_active: A boolean field indicating whether the user
        is an active user.
        - date_joined: A DateTimeField representing when the user
        joined the site.
    """
    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        """
        Return a string representation of the user (user's email address).
        """
        return self.email
