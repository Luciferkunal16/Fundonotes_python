import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializer import NotesSerializer
from .utils import verify_token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db import connection
from datetime import datetime

cursor = connection.cursor()

logging.basicConfig(filename="note.log", level=logging.INFO)


class Notes(APIView):

    @swagger_auto_schema(
        operation_summary="Add",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description"),
            }
        ),
    )
    @verify_token
    def post(self, request):
        """
        For creating a new Note for a user
        :param request:
        :return:Response
        """

        try:
            cursor.execute('INSERT into notes_note (title,description,user_id_id,created_at) values (%s,%s,%s,%s)',
                           [request.data.get('title'), request.data.get('description'), request.data.get('user_id'),
                            datetime.now()])
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # serializer.save()

            return Response({"message": "Note Created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": "Note Creation Unsuccessfull", "error": "{}".format(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="get",
    )
    @verify_token
    def get(self, request):
        """
        For getting a specified note of user
        :param request:
        :return: Response
        """
        try:
            for notes in Note.objects.raw(
                    'SELECT id,description from notes_note where user_id_id= %s', [request.data.get('user_id')]):
                print(notes.title, " ", notes.description)

            note = Note.objects.filter(user_id=request.data.get("user_id"))
            serializer = NotesSerializer(note, many=True)

            return Response(
                {"message": "Your Notes are Found", "data": serializer.data},
                status=status.HTTP_302_FOUND)

        except Exception as e:
            logging.error(e)
            print(e)
            return Response({"message": "Your Notes are not Found"})

    @swagger_auto_schema(
        operation_summary="update ",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description="title"),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description="description"),
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="note id"),
            }
        ),
    )
    @verify_token
    def put(self, request):
        """
        To update a previous note
        :param request:
        :return:
        """
        try:
            cursor.execute(
                'UPDATE  notes_note SET title = %s,description=%s,created_at=%s WHERE user_id_id=%s AND id=%s',
                [request.data.get('title'), request.data.get('description'), datetime.now(),
                 request.data.get('user_id'),
                 request.data.get('id')])

            note = Note.objects.get(id=request.data["id"])
            serializer = NotesSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            # serializer.save()

            return Response({"message": "Note Updated", "Data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            logging.error(e)
            return Response({"message": "Note Updation Unsuccesfull", "error": "{}".format(e)},
                            status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Delete",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'id': openapi.Schema(type=openapi.TYPE_INTEGER, description="note id"),
            }
        ),
    )
    @verify_token
    def delete(self, request):
        """
        For deleting a Existing Note
        :param request:
        :return:
        """
        try:
            cursor.execute( 'DELETE FROM notes_note WHERE id=%s', [request.data.get('id')])

            # note = Note.objects.get(pk=request.data["id"])

            # note.delete()

            return Response({"message": "Note Deleted "},
                            status=status.HTTP_200_OK)
        except Exception as e:
            logging.exception(e)
            return Response({
                "message": "Note Deletion Unsuccessfull", "error": "{}".format(e)
            }, status=status.HTTP_400_BAD_REQUEST)
