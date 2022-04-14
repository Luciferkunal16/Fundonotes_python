from django.urls import path

from . import views

app_name = 'note'
urlpatterns = [
    path('note', views.Notes.as_view(), name='note'),
    path('notesdelete/<int:id>', views.NotesDetails.as_view(), name='notedelete'),
    path('label',views.add_label,name="label")
]
