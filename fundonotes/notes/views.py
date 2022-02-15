import logging

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Note

from .serializer import NotesSerializer
from .utils import verify_token

logging.basicConfig(filename="note.log", level=logging.INFO)


class Notes(APIView):

    @verify_token
    def post(self, request):
        """
        For crating a new Note for a user
        :param request:
        :return:Response
        """

        try:
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"message": "Note Created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Note Creation Unsuccessfull", "error": "{}".format(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def get(self, request):
        """
        For getting a specified note of user
        :param request:
        :return: Response
        """
        try:
            note = Note.objects.filter(user_id=request.data.get("user_id"))
            serializer = NotesSerializer(note, many=True)
            return Response(
                {"message": "Your Notes are Found", "data": serializer.data},
                status=status.HTTP_302_FOUND)

        except Exception as e:
            logging.error(e)
            return Response({"message": "Note Not Found", "Error": {}.format(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def put(self, request):
        """
        To update a previous note
        :param request:
        :return:
        """
        try:
            note = Note.objects.get(id=request.data["id"])
            serializer = NotesSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"Message": "Note Updated", "Data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return Response({"message": "Note Updation Unsuccesfull","error":"{}".format(e)}, status=status.HTTP_400_BAD_REQUEST)

    @verify_token
    def delete(self, request):
        """
        For deleting a Existing Note
        :param request:
        :return:
        """
        try:
            note = Note.objects.get(pk=request.data["id"])
            note.delete()
            return Response({"message": "Note Deleted ", "status": status.HTTP_204_NO_CONTENT},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({
                "message": "Note Deletion Unsuccessfull", "error": "{}".format(e)
            }, status=status.HTTP_400_BAD_REQUEST)
