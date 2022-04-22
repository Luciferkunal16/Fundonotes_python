from rest_framework.response import Response
from user.utils import EncodeDecodeToken


def verify_token(function):
    """
    this function is created for verifying user
    """

    def wrapper(self, request, note_id=None):
        print(note_id)
        if 'HTTP_AUTHORIZATION' not in request.META:
            resp = Response({'message': 'Token not provided in the header'})
            resp.status_code = 401
            return resp
        token = request.META['HTTP_AUTHORIZATION']
        user_id = EncodeDecodeToken.decode_token(token)
        request.data.update({'user_id': user_id.get("user_id")})
        if note_id is None:
            return function(self, request)
        else:
            return function(self, request, note_id)

    return wrapper
