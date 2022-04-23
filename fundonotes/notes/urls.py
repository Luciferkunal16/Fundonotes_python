from django.urls import path

from . import views

app_name = 'note'
urlpatterns = [
    path('note', views.DetailedNoteMixin.as_view(), name='note'),
    path('note/<int:pk>', views.DetailedNoteMixin.as_view(), name='delete'),


]
