from unittest import TestCase
#
# from  import AUTH_USER_MODEL, INSTALLED_APPS
import pytest
from mixer.auto import mixer
from ..models import User

pytestmark = pytest.mark.django_db
from ..models import User


class TestUser:

    def test_init(self):
        user_obj = mixer.blend((User))
        assert user_obj.pk == 1

    @pytest.mark.django_db
    def test_create(self):
        data = {"username": "arun", "password": "arun", "email": "arun@gmail.com", "phone_number": "231132312",
                "is_verified": "True"}
        user_obj = User.objects.create_user(**data)
        assert user_obj.username == 'arun'
        assert user_obj.email == 'arun@gmail.com'
