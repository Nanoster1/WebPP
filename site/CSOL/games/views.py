from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Game


class GameDetailView(DetailView):
    model = Game
    context_object_name = 'game'
    template_name = 'games/game_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = '{} | CSOL'.format(context['object'].title)
        return context


class GameListViews(ListView):
    model = Game
    template_name = "games/index.html"
    context_object_name = 'games_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'CSOL - Играй бесплатно!'
        return context
