from django.contrib.auth import views
from django.urls import path

from .views import *

app_name = 'accounts'
urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path(r'update/<str:slug>/', UpdateProfile.as_view(), name='update_user'),
]