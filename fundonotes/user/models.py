from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    phone_number = models.CharField(max_length=10, unique=False)
    is_verified = models.BooleanField(default=False)


