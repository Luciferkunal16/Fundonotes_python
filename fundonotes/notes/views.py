import logging
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, mixins, generics
from .models import Note
from .serializer import NotesSerializer
from .utils import verify_token
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

logging.basicConfig(filename="note.log", level=logging.INFO)

class DetailedNoteMixin(mixins.UpdateModelMixin,
                        mixins.ListModelMixin,
                        mixins.CreateModelMixin,
                        generics.GenericAPIView,
                        mixins.DestroyModelMixin):
    queryset = Note.objects.all()
    serializer_class = NotesSerializer

    def list(self, request, *args, **kwargs):
        queryset = Note.objects.filter(user_id=request.data.get("user_id"))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, *args, **kwargs):
        print(request.data)
        return self.update(request)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request)
