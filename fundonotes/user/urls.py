from django.urls import path

from . import views

urlpatterns = [
    path('registration', views.UserRegistration.as_view(), name='registration'),
    path('login', views.UserLogin.as_view(), name='login'),
    path('validate/<str:token>',views.ValidateToken.as_view(),name='validate')

]
