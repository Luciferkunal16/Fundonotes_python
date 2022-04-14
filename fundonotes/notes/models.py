from datetime import datetime

from django.db import models

# noinspection PyUnresolvedReferences
from user.models import User


class Note(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)
    archive = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    color = models.CharField(max_length=100, default='#FFFFFF')


class Label(models.Model):
    name = models.CharField(max_length=100)
    color_id = models.CharField(max_length=100)
    note = models.ManyToManyField(Note)
