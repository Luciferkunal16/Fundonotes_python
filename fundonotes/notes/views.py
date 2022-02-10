import logging

from django.http import HttpResponse, request, Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Note

from .serializer import NoteSerializer

logging.basicConfig(filename="note.log", level=logging.INFO)


class CreateNote(APIView):
    def get(self, request, format=None):
        """
        for retriving all the notes in database
        :param request:
        :param format:
        :return:
        """
        note = Note.objects.all()
        serializer = NoteSerializer(note, many=True)

        return Response(serializer.data)

    def post(self, request):
        """
        For creating the new Note in database
        :param request:
        :return:
        """
        try:
            serializer = NoteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Note Created", "data": serializer.data,
                             "status": "status={}".format(status.HTTP_201_CREATED)})
        except Exception as e:
            print(e)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NoteDetail(APIView):
    """
    Retrieve, update or delete a Note instance.
    """

    def get_object(self, pk):
        try:
            return Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        """
        geting specific note by giving note id
        :param request:
        :param pk:
        :param format:
        :return:
        """
        note = self.get_object(pk)
        serializer = NoteSerializer(note)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        """
        for Updating the note by giving userid
        :param request:
        :param pk:
        :param format:
        :return:
        """
        try:
            note = self.get_object(pk)
            serializer = NoteSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"Message": "Note Updated", "Data": serializer.data})
        except Exception as e:
            logging.error(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        """
        For deleting the note by giving note id
        :param request:
        :param pk:
        :param format:
        :return:
        """
        try:
            note = self.get_object(pk)
            note.delete()
            return Response({"message": "Note Deleted ", "status": status.HTTP_204_NO_CONTENT})
        except Exception as e:
            logging.exception(e)
            return Response({"Error": e})
