from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Game


class GameDetailView(DetailView):
    model = Game
    context_object_name = 'game'
    template_name = 'games/game_detail.html'


class GameListViews(ListView):
    model = Game
    template_name = "games/index.html"
    context_object_name = 'games_list'
