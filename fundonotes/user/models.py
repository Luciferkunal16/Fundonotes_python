from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

class User(AbstractUser):
    phone_number = models.CharField(max_length=10, unique=False)
    is_verified = models.BooleanField(default=False)


class LogTable(models.Model):
    hit_time = models.DateTimeField(default=datetime.now, blank=True)
    type_of_request = models.CharField(max_length=250)
    response = models.CharField(max_length=200)
