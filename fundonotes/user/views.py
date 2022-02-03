import json
from .models import User
from django.http import HttpResponse


def registration(request):
    """
    for registration of new user.
    add new entries to Database
    :param request:
    :return:
    """
    user_dict = json.loads(request.body)
    users = User.objects.all()
    for user in users:
        if user_dict.get("username") == user.username:
            return HttpResponse("User is already Registered")

    username = user_dict.get("username")
    password = user_dict.get("password")
    email = user_dict.get("email")
    phone_number = user_dict.get("phonenumber")
    is_verified = user_dict.get("is_verified")
    user = User(username=username, password=password, email=email, phonenumber=phone_number, is_verified=is_verified)
    user.save()
    return HttpResponse("User Registered Successfully")


def login(request):
    """
    For login of user
    :param request:
    :return:
    """
    user_dict = json.loads(request.body)
    users = User.objects.all()
    for user in users:
        if user_dict.get("username") == user.username and user_dict.get("password") == user.password:
            return HttpResponse("Login Successfull")

    return HttpResponse("Login Failed Invalid Credentials!!!")


def retrive(request):
    """
    for retriving all the data from database
    :param request:
    :return:
    """
    users = User.objects.all()
    list_of_user = list()
    for user in users:
        dict_of_user = {"username": user.username, "password": user.password, "email": user.email,
                        "phonenumber": user.phonenumber, "is_verified": user.is_verified}
        list_of_user.append(dict_of_user)
    return HttpResponse(list_of_user)
