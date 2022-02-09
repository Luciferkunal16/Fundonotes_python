import json
import logging

from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from .serializers import UserSerializer

User = get_user_model()

logging.basicConfig(filename="user.log", level=logging.INFO)


class UserRegistration(APIView):

    def post(self, request):
        """
        :Description:
        for registration of new user.
        add new entries to Database
        :param request:
        :return:Jsonresponse
        """
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                # serializer.save()

                #     return Response(serializer.data, status=status.HTTP_201_CREATED)
                # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
                if user:
                    return JsonResponse({"message": "User Already Registered"})
                new_user = User.objects.create_user(username=serializer.data['username'],
                                                    password=serializer.data['password'],
                                                    email=serializer.data['email'],
                                                    phone_number=serializer.data['phone_number'],
                                                    is_verified=serializer.data['is_verified']
                                                    )

                new_user.save()
                return JsonResponse(
                    {"message": "User Registered Successfully ", "data": "User name is {}".format(new_user.username)},
                    safe=False)
                logging.debug("Registration Successfull")
        except Exception as e:
            print(e)
            logging.error(e)
            return HttpResponse(e)


class UserLogin(APIView):
    def post(self, request):
        """
        For login of user
        :param request:
        :return:Httpresponse
        """
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():

                user = authenticate(username=serializer.data['username'], password=serializer.data['password'])
                if user:
                    return JsonResponse({"message": "Login Successfull!!"}, safe=False)
                return JsonResponse({"message": "Login Failed Invalid Credentials!!!"}, safe=False)
        except Exception as exc:
            logging.error(exc)
            return HttpResponse("error is {}".format(exc))
