from datetime import datetime

from rest_framework import serializers
from .models import Note


class NotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"

    def create(self, validate_data):

        notes = Note.objects.create(
            title=validate_data.get("title"),
            description=validate_data.get("description"),
            user_id=validate_data.get("user_id"),
            color=validate_data.get('color'),
            archive=validate_data.get('archive'),
            is_deleted=validate_data.get('is_deleted')


        )
        return notes
