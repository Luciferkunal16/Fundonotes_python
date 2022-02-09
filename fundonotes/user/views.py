import json
import logging

from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

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
            user_dict = json.loads(request.body)
            user = authenticate(username=user_dict.get("username"), password=user_dict.get("password"))
            if user:
                return JsonResponse({"message": "User Already Registered"})
            new_user = User.objects.create_user(username=user_dict.get("username"),
                                                password=user_dict.get("password"), email=user_dict.get("email"),
                                                phone_number=user_dict.get("phone_number"),
                                                is_verified=user_dict.get("is_verified")
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
            user_dict = json.loads(request.body)
            user = authenticate(username=user_dict.get("username"), password=user_dict.get("password"))
            if user:
                return JsonResponse({"message": "Login Successfull!!"}, safe=False)
            return JsonResponse({"message": "Login Failed Invalid Credentials!!!"}, safe=False)
        except Exception as exc:
            logging.error(exc)
            return HttpResponse("error is {}".format(exc))
