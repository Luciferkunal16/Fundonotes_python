import json
import logging
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.contrib.auth import get_user_model, authenticate
from .utils import EncodeDecodeToken
from .task import send_email
from .serializers import UserSerializer

logging.basicConfig(filename="user.log", level=logging.INFO)


class UserRegistration(APIView):

    def post(self, request):
        """
        :Description:
        for registration of new user.
        add new entries to Database
        :param request:
        :return:response
        """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = User.objects.filter(username=serializer.data['username'])
            if user:
                return Response({"message": "User Already Registered"},
                                status=status.HTTP_400_BAD_REQUEST)
            new_user = User.objects.create_user(username=serializer.data['username'],
                                                password=serializer.data['password'],
                                                email=serializer.data['email'],
                                                phone_number=serializer.data['phone_number'],

                                                )

            encoded_token = EncodeDecodeToken.encode_token(payload=new_user.pk)
            send_email.delay(token=encoded_token, to=serializer.data['email'], name=serializer.data['username'])
            logging.debug("Registration Successfull")
            return Response(
                {
                    "message": "User Registered Successfully ",

                }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            logging.error(e)
            return Response(
                {
                    "message": "data storing failed"
                }, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    def post(self, request):
        """
        For login of user
        :param request:
        :return:response
        """
        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = authenticate(username=serializer.data['username'], password=serializer.data['password'])

            if user and user.is_verified == True:
                token = EncodeDecodeToken.encode_token(payload=user.pk)
                return Response({"message": "Login Successfull!!", "token": "{}".format(token)},
                                status=status.HTTP_201_CREATED)

            return Response({
                "message": "login Unsuccessfull"
            },
                status=status.HTTP_404_NOT_FOUND)
        except Exception as exc:
            print(exc)
            logging.error(exc)
            return Response({"error": "{}".format(exc)}, status=status.HTTP_400_BAD_REQUEST)


class ValidateToken(APIView):
    def get(self, request, token):
        """
        use to validate the user and verify the user
        :param token:
        :return:Response
        """
        try:

            decoded_token = EncodeDecodeToken.decode_token(token=token)
            user = User.objects.get(id=decoded_token.get('user_id'))
            user.is_verified = True
            user.save()

            return Response({"message": "Validation Successfull"},
                            status=status.HTTP_201_CREATED)
        except Exception as e:
            logging.error(e)
            return HttpResponse(e)
