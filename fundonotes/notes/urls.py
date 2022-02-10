from django.urls import path

from . import views

urlpatterns = [
    path('note', views.CreateNote.as_view()),
    path('note/<int:pk>', views.NoteDetail.as_view()),
]
