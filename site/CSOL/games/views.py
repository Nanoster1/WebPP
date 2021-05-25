from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, ListView

from .models import Game, CategoryGame


class GameDetailView(DetailView):
    model = Game
    context_object_name = 'game'
    template_name = 'games/game_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        Game.objects.get(slug=self.kwargs['slug']).add_view_user()
        context['title'] = '{} | CSOL'.format(context['object'].title)
        return context


class GameListViews(ListView):
    model = Game
    template_name = "games/index.html"
    context_object_name = 'games_list'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = CategoryGame.objects.all()
        context['title'] = 'CSOL - Играй бесплатно!'
        context['categories'] = categories
        return context


class GameCategoryListViews(GameListViews):
    model = CategoryGame

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        name = CategoryGame.objects.get(slug=self.kwargs['slug'])
        context['title'] = 'Категория:  {} | CSOL - Играй бесплатно!'.format(name)
        return context

    def get_queryset(self):
        return Game.objects.filter(category__slug=self.kwargs['slug'])


class GameNewListViews(GameListViews):

    def get_queryset(self):
        return Game.objects.all().order_by('-date_added')


class GamePopularListViews(GameListViews):

    def get_queryset(self):
        return Game.objects.all().order_by('-user_views')
