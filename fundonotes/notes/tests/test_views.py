import json

import pytest as pytest
from rest_framework import status
from rest_framework.reverse import reverse
from ..models import Note
from django.test import TestCase, Client
# noinspection PyUnresolvedReferences
from user.models import User

client = Client()

# pyjwt
class GetSingleNote(TestCase):
    """ Test module for GET single Note API """

    @pytest.mark.django_db
    def setUp(self):
        self.user = User.objects.create_user(id=1, username="kunal", password="kunal", email="wda",
                                             phone_number="12345678", is_verified="True")
        self.user.save()
        self.note = Note.objects.create(title="test", description="test", user_id=self.user.id)

    @pytest.mark.django_db
    def test_get_valid_all_notes(self):
        response = client.get(reverse('note:note'))
        print(self.user)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_post_notes(self):
        url = reverse('note:note')
        response = client.post(url, {'title': 'new idea', "description": "test", "user_id": "2"}, format='json')
        assert response.status_code == status.HTTP_201_CREATED

  # def test_get_single_note(self):
    #     respone=client.get(reverse('note:note/1'))
    #     assert respone.status_code == 201
