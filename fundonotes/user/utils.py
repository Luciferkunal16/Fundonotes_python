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
