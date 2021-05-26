from django.contrib.auth import views
from django.urls import path

from .views import *

app_name = 'accounts'
urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('profile/edit', profile_edit, name='profile_edit'),
    path('profile/id<int:user_id>', ProfileDetailView.as_view(), name='profile'),
]