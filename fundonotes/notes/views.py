import logging, json
from .utils import get_note_with_label
from django.http import JsonResponse
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Note, Label
from .serializer import NotesSerializer
from .utils import verify_token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

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
            serializer = NotesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

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
            note = Note.objects.filter(user_id=request.data.get("user_id"))

            serializer = NotesSerializer(note, many=True)
            data=get_note_with_label(serializer)
            return Response(
                {"message": "Your Notes are Found", "data": data},
                status=status.HTTP_200_OK)

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
            note = Note.objects.get(id=request.data["id"])
            serializer = NotesSerializer(note, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

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
        ), )
    @verify_token
    def delete(self, request, note_id):
        """
                        delete note of user
                        :param note_id: note_id
                        :param request:
                        :return:response
                        """
        try:
            note = Note.objects.get(pk=note_id)
            print(note)
            note.delete()
            return Response({
                "message": "Note delete successfully"
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            print("reach Exception")
            return Response(
                {
                    "message": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST)


class Labels(APIView):

    def post(self, request):
        try:
            label = Label(name=request.data.get('name'), color=request.data.get('color'))
            label.save()
            label.note.add(request.data.get('note_id'))
            return JsonResponse({"message": "label Added "})
        except Exception as err:
            return  JsonResponse({"message":"Exception occurred ","error":str(err)})
