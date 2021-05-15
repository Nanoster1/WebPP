from django.urls import path

from .views import *

app_name = 'games'
urlpatterns = [
    path('', GameListViews.as_view(), name='index'),
    path('<str:slug>/', GameDetailView.as_view(), name='game_detail'),
]
