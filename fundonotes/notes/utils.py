from rest_framework.response import Response
from user.utils import EncodeDecodeToken
import json
from .models import Label


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


def get_note_with_label(serializer):
    notes = json.loads(json.dumps(serializer.data))
    list_of_notes = list()
    for note in notes:
        labels = Label.objects.filter(note=note.get('id'))
        list_of_labels = list()
        for label in labels:
            l = {"name": label.name, "color": label.color}
            list_of_labels.append(l)
        note.update({"label":list_of_labels})
        list_of_notes.append(note)

    return list_of_notes
