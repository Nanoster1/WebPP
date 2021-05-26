from django.urls import path

from .views import *

app_name = 'games'
urlpatterns = [
    path('', GameListViews.as_view(), name='game_list_all'),
    path('news/', GameNewListViews.as_view(), name='game_news'),
    path('popular/', GamePopularListViews.as_view(), name='game_popular'),
    path('category/<str:slug>/', GameCategoryListViews.as_view(), name='game_category'),
    path('comment/<int:game_id>/', add_comment, name='add_comment'),
    path('<str:slug>/', GameDetailView.as_view(), name='game_detail'),
]
