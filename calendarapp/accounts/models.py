from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from timezone_utils.choices import COMMON_TIMEZONES_CHOICES

from .managers import UserManager


class User(AbstractUser):
    objects = UserManager()

    email = models.EmailField(blank=False,
                              unique=True,
                              help_text='Required.')
    timezone = models.CharField(max_length=255,
                                choices=COMMON_TIMEZONES_CHOICES,
                                default=settings.TIME_ZONE)
