import json

import pytest as pytest
from django.test import TestCase, Client
from unittest import TestCase

from rest_framework.reverse import reverse

from ..models import User

client = Client()


class TestLogin(TestCase):

    @pytest.mark.django_db
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='kunal', email='kunal@gmail,com',
                                             phone_number='9191919191', is_verified='True')

    @pytest.mark.django_db
    def test_registration(self):
        response = client.post(reverse('registration'),
                               {'username': 'test2', 'password': 'test2', 'email': 'dwwad', 'phone_number': '12345679',
                                'is_verified': 'True'}, format='json')
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_login(self):
        respone = client.post(reverse('login'), {'username': 'test', 'password': 'kunal'}, format='json')

        assert respone.status_code == 201
