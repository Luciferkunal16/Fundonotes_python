from django.urls import path

from . import views

app_name = 'note'
urlpatterns = [
    path('note', views.Notes.as_view(), name='note'),
    path('note/<int:note_id>', views.Notes.as_view(), name='delete'),
    path('label',views.Labels.as_view(),name="label")
]
