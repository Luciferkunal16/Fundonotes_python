# import pytest
# from mixer.backend.django import mixer
# from ..models import Note
# pytestmark = pytest.mark.django_db
# from user.models import User
#
# class TestNote:
#     def test_init(self):
#         note_obj = mixer.blend(('notes.Note'))
#         assert note_obj.pk == 1
#
#
#     @pytest.mark.django_db
#     def test_create(self):
#         user=User.objects.create_user(username="kunalt",password="kunalt",email="wda",phone_number="12345678",is_verified="True")
#         user.save()
#
#         data = {"title": "test", "description": "desc", "user_id": user.pk}
#         note_obj = Note.objects.create(**data)
#
#         assert note_obj.username == 'arun'
#         assert note_obj.email == 'arun@gmail.com'
