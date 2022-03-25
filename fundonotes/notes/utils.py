from rest_framework.response import Response
from user.utils import EncodeDecodeToken


def verify_token(function):
    """
    this function is created for verifying user
    """

    def wrapper(self, request,*args,**kwargs):
        if 'HTTP_AUTHORIZATION' not in request.META:
            resp = Response({'message': 'Token not provided in the header'})
            resp.status_code = 400
            return resp
        token = request.META['HTTP_AUTHORIZATION']
        user_id = EncodeDecodeToken.decode_token(token)
        request.data.update({'user_id': user_id.get("user_id")})
        return function(self, request)

    return wrapper


