from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.template.context_processors import csrf
from django.views.decorators.http import require_http_methods
from django.views.generic import DetailView, ListView

from .forms import CommentForm
from .models import Game, CategoryGame, Comment


class GameDetailView(DetailView):
    model = Game
    context_object_name = 'game'
    template_name = 'games/game_detail.html'
    comment_form = CommentForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(csrf(self.request))
        context['object'].add_view_user()
        user = auth.get_user(self.request)
        context['comments'] = context['object'].comment_set.all()
        # .order_by('path')
        if user.is_authenticated:
            context['form'] = self.comment_form
        context['title'] = '{} | CSOL'.format(context['object'].title)
        return context


@login_required
@require_http_methods(["POST"])
def add_comment(request, game_id):
    form = CommentForm(request.POST)
    game = get_object_or_404(Game, id=game_id)

    if form.is_valid():
        comment = Comment(
            # path=[],
            game_id=game,
            author_id=request.user,
            content=form.cleaned_data['comment_area']
        )
        comment.save()

        # try:
        #     print('проверка')
        #     # comment.path.extend(Comment.objects.get(id=form.cleaned_data['parent_comment']).path)
        #     comment.path.append(comment.id)
        # except ObjectDoesNotExist:
        #     comment.path.append(comment.id)

        comment.save()

    return redirect(game.get_absolute_url())


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
