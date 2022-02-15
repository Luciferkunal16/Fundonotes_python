from datetime import datetime

from django.db import models

# noinspection PyUnresolvedReferences
from user.models import User


class Note(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    created_at = models.DateTimeField(default=datetime.now, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.PROTECT)

