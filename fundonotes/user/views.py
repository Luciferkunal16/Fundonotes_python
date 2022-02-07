import json
import logging

from .models import User
from django.http import HttpResponse
from django.http import JsonResponse

logging.basicConfig(filename="user.log", level=logging.INFO)


def registration(request):
    """
    :Description:
    for registration of new user.
    add new entries to Database
    :param request:
    :return:Httpresponse
    """
    try:

        user_dict = json.loads(request.body)
        user = User.objects.filter(username=user_dict.get("username"), password=user_dict.get("password")).exists()
        if user:
            return JsonResponse({"message": "User Already Registered"})
        new_user = User(username=user_dict.get("username"), password=user_dict.get("password"),
                        email=user_dict.get("email"),
                        phonenumber=user_dict.get("phonenumber"), is_verified=user_dict.get("is_verified"))
        new_user.save()
        return JsonResponse(
            {"message": "User registered successfully", "data": "username:{}".format(new_user.username)})
        logging.debug("Registration Successfull")
    except Exception as exc:
        logging.error(exc)
        return JsonResponse({"Error": exc})


def login(request):
    """
    For login of user
    :param request:
    :return:Httpresponse
    """
    try:
        user_dict = json.loads(request.body)
        user = User.objects.filter(username=user_dict.get("username"), password=user_dict.get("password")).exists()
        if user :
            return JsonResponse({"message": "Login Successfull!!"})
        return JsonResponse({"message": "Login Failed Invalid Credentials!!!"})
    except Exception as exc:
        print(exc)
        logging.error(exc)
        return JsonResponse({"Error": exc})

