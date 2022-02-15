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


class Email:
    @staticmethod
    def send_email( to,token,name ):
        send_mail(from_email=settings.EMAIL_HOST, recipient_list=[to],
                  message="Hy {}\n Welcome to Fundonotes App ,Thanks for installing our software\n Your Activation url = "
                          "http://127.0.0.1:8000/user/validate/{}".format( name,
                      token),
                  subject="Link for Your Registration", fail_silently=False, )
