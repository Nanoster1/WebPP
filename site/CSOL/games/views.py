from django.shortcuts import render
from django.views.generic import DetailView

from .models import Game


def index(request):
    return render(request, 'games/index.html', {'title': 'Главная | CSOL', })


class GameDetailView(DetailView):

    model = Game
    context_object_name = 'game'
    template_name = 'games/game_detail.html'

