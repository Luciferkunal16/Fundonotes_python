import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializer import NotesSerializer
from .utils import verify_token
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions

logging.basicConfig(filename="note.log", level=logging.INFO)

import logging

logging.basicConfig(filename="views.log", filemode="w")


class Notes(ListCreateAPIView):
    queryset = Note.objects.all()
    serializer_class = NotesSerializer
    print(queryset)

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.data.get("user_id"))

    def perform_create(self, serializer):
        return serializer.save(id=self.request.data)


class NotesDetails(RetrieveUpdateDestroyAPIView):
    serializer_class = NotesSerializer
    queryset = Note.objects.all()
    lookup_field = 'id'
