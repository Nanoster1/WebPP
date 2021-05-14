from django.urls import path

from .views import index, GameDetailView

app_name = 'games'
urlpatterns = [
    path('', index, name='index'),
    path('<str:slug>/', GameDetailView.as_view(), name='game_detail'),
]
