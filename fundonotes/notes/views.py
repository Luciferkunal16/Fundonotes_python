import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializer import NotesSerializer
from .utils import verify_token
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

logging.basicConfig(filename="note.log", level=logging.INFO)

logging.basicConfig(filename="views.log", filemode="w")


class Notes(ListCreateAPIView):
    queryset = Note.objects.all()

    @verify_token
    def list(self, request):
        """
        For geting list of Notes
        """
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset(request)
        serializer = NotesSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self, request):
        return self.queryset.filter(user_id=request.data.get("user_id"))

    @verify_token
    def create(self, request):
        """
        For creating the  note
        """
        Noteserializer = self.get_serializer_class()
        serializer = Noteserializer(data=request.data)
        serializer.is_valid(True)
        serializer.save(id=self.request.data.get("id"))
        return Response({"message": "Note creaed Successfully", "data": serializer.data})

    def get_serializer_class(self):
        return NotesSerializer


class NotesDetails(RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    lookup_field = "id"

    @verify_token
    def update(self, request, *args, **kwargs):
        """
        For Updating the existing Note
        """
        note_object = self.get_object()
        note = Note.objects.filter(id=note_object.id, user_id=request.data.get('user_id')).first()
        serializer = self.get_serializer_class()
        note_serializer = serializer(note, data=request.data)
        note_serializer.is_valid()
        note_serializer.save()

        return Response({"message": "Note Updated Successfull", "data": note_serializer.data})

    def get_serializer_class(self):
        return NotesSerializer

    @verify_token
    def destroy(self, request, *args, **kwargs):
        """
        Used for Deleting the Note by giving Note id
        """
        note_object = self.get_object()
        note = Note.objects.filter(id=note_object.id, user_id=request.data.get('user_id'))
        note.delete()

        return Response({"message": "Note Deleted"}, status=status.HTTP_204_NO_CONTENT)
