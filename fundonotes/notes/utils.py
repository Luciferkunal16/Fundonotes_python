from rest_framework.response import Response
from user.utils import EncodeDecodeToken
import json
from .models import Label
from .serializer import LabelSerializer


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


def get_note_with_label(notes):
    """
    for formatting the get note to imclude label in it
    """
    try:
        list_of_notes = list()
        for note in notes:
            label = LabelSerializer(note.label_name.all(), many=True)
            note_data = {"id": note.id, "title": note.title, 'description': note.description,
                         'created_at': note.created_at,
                         'archive': note.archive, 'color': note.color, "labels": label.data}
            list_of_notes.append(note_data)
        return list_of_notes
    except Exception as e:
        print(e)
