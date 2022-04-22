import logging
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from django.contrib.auth import authenticate
from .utils import EncodeDecodeToken, email_error
from .task import send_email
from .serializers import UserSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import re
from .utils import email_error, EmailService
from rest_framework.exceptions import ValidationError

logging.basicConfig(filename="user.log", level=logging.INFO)


class UserRegistration(APIView):
    @swagger_auto_schema(
        operation_summary="register",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
                # 'phone_number': openapi.Schema(type=openapi.TYPE_STRING, description='phone_number'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='first_name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='last_name'),

            }
        ))
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
                return Response({"message": "User Already Registered"}, status=status.HTTP_400_BAD_REQUEST)
            new_user = User.objects.create_user(username=serializer.data['username'],
                                                password=serializer.data['password'],
                                                email=serializer.data['email'],
                                                first_name=serializer.data['first_name'],
                                                last_name=serializer.data['last_name']
                                                )

            encoded_token = EncodeDecodeToken.encode_token(payload=new_user.pk)
            logging.debug("Registration Successfully")
            return Response(
                {
                    "message": "User Registration Successfull ", "token": encoded_token

                }, status=status.HTTP_201_CREATED)
        except email_error:
            logging.error("Wrong email Address")
            return Response(
                {
                    "message": "Wrong email Address"
                },
                status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            logging.error("Validation failed")
            return Response(
                {
                    "message": "validation failed"
                },
                status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            logging.error(e)
            return Response(
                {
                    "message": "data storing failed"
                }, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    @swagger_auto_schema(
        operation_summary="login",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='username'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='password'),
            }
        ))
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
