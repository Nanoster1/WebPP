from django.contrib.auth import views
from django.urls import path

from .views import login, register

app_name = 'accounts'
urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
]