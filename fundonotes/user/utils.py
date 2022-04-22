from aifc import Error

import jwt
from django.core.mail import send_mail
from fundonotes import settings

class EncodeDecodeToken:
    """
    For  Encoding and Decoding User
    """

    @staticmethod
    def encode_token(payload):
        encoded_token = jwt.encode({"user_id": payload},
                                   "secret",
                                   algorithm="HS256"
                                   )
        return encoded_token

    @staticmethod
    def decode_token(token):
        decoded_token = jwt.decode(
            token,
            "secret",
            algorithms="HS256"
        )
        return decoded_token


class Error(Exception):
    # Error is derived class for Exception, but
    # Base class for exceptions in this module
    pass


class email_error(Error):
    pass


class EmailService:
    @staticmethod
    def send_email(to, token, name):
        """
        to send the email to desired user
        :param to:
        :param token:
        :param name:
        :return:
        """
        send_mail(from_email=settings.EMAIL_HOST, recipient_list=[to],
                  message="Hy {}\nWelcome to Fundonotes App ,Thanks for installing our software\nYour Activation url = "
                          "http://127.0.0.1:8000/user/validate/{}".format(name,
                                                                          token),
                  subject="Link for Your Registration", fail_silently=False, )
