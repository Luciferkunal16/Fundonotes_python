from datetime import datetime

from rest_framework import serializers
from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['title', 'description', 'user_id', 'created_at']
        optional_fields = ['user_id', 'created_at']

# class NoteSerializer(serializers.Serializer):
#     user_id = serializers.IntegerField(read_only=True)
#     created_at=serializers.DateTimeField(default=datetime.now)
#     title=serializers.CharField(required=True )
#     description=serializers.CharField(required=True)
#
#     def create(self, validated_data):
#         """
#         Create and return a new `Snippet` instance, given the validated data.
#         """
#         return Note.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Snippet` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.description = validated_data.get('description', instance.description)
#         instance.created_at = validated_data.get('created_at', instance.created_at)
#         instance.user_id = validated_data.get('user_id', instance.user_id)
#         instance.save()
#         return instance
