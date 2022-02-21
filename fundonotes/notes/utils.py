import json
import logging

from django.http import QueryDict
from rest_framework.response import Response
from user.utils import EncodeDecodeToken
from .redis_service import RedisService


def verify_token(function):
    """
    this function is created for verifying user
    """

    def wrapper(self, request):
        if 'HTTP_AUTHORIZATION' not in request.META:
            resp = Response({'message': 'Token not provided in the header'})
            resp.status_code = 400
            return resp
        token = request.META['HTTP_AUTHORIZATION']
        user_id = EncodeDecodeToken.decode_token(token)
        request.data.update({'user_id': user_id.get("user_id")})
        return function(self, request)

    return wrapper


class RedisOpertions:
    def __init__(self):
        self.cache_memory = RedisService()

    def add_note(self, note):
        """
        for adding the note to cache memory
        :param note:
        :return:
        """
        try:
            user_id = int(note.get("user_id"))
            existing_note = self.get_note(user_id)
            dict_of_note = {user_id: existing_note}
            if existing_note is None:
                inside_dict = {int(note.get("id")): json.dumps(note)}
                dict_of_note[user_id] = inside_dict
                self.cache_memory.set(user_id, json.dumps(dict_of_note[user_id]))
            else:
                inside_dict = {int(note.get("id")): json.dumps(note)}
                appened_note = {**existing_note, **inside_dict}
                self.cache_memory.set(user_id, json.dumps(appened_note))

        except Exception as err:
            logging.error(err)

    def get_note(self, user_id):
        """
        for getting the notes from cache memory
        :param note:
        :return:
        """

        try:

            return json.loads(self.cache_memory.get(user_id))
        except Exception as err:
            print(err)
            logging.error(err)

    def update_note(self, updated_note):
        """
        For Updating the existing notes
        :param updated_note:
        :return:
        """
        try:
            user_id = updated_note.get("user_id")
            list_of_note = json.loads(self.cache_memory.get(user_id))

            if list_of_note.get(str(updated_note.get("id"))):
                list_of_note.update({str(updated_note.get("id")): updated_note})
                self.cache_memory.set(user_id, json.dumps(list_of_note))
            else:
                print("No Note of specified ID")

        except Exception as e:
            print(e)

    def delete_note(self, id, user_id):
        """
        For Deleting the note from the redis server
        :param id:
        :param user_id:
        :return:
        """

        try:
            list_of_note = json.loads(self.cache_memory.get(user_id))
            if list_of_note.get(str(id)):
                list_of_note.pop(str(id))
                self.cache_memory.put(user_id, json.dumps(list_of_note))
            else:
                print("Note not found or Wrong Note Id ")
        except Exception as e:
            print(e)
            logging.error(e)

