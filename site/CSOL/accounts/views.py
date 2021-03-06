from django.contrib.auth import (login as auth_login, authenticate)
from django.contrib.auth import logout as user_logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import DetailView

from .models import Profile


def login(request):
    template = 'registration/login.html'

    message = None
    title = 'Авторизация | CSOL'
    if request.method == 'POST':
        _username = request.POST['username']
        _password = request.POST['password']
        user = authenticate(username=_username, password=_password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                message = 'Ваш аккаунт не активирован!'
        else:
            message = 'Неправильно введен логин или пароль.'
    context = {'message': message,
               'title': title}
    return render(request, template, context)


def register(request):
    template = 'registration/register.html'

    message = None
    title = 'Регистрация | CSOL'

    if request.method == 'POST':
        _username = request.POST['username']
        _email = request.POST['email']
        _password1 = request.POST['password1']
        _password2 = request.POST['password2']

        if not (_username and _email and _password2 and _password1):
            message = 'Заполните все поля!'
        elif User.objects.filter(username=_username).exists():
            message = 'Такой пользователь уже существует!'
        elif _password1 != _password2:
            message = 'Неправильно введен повторный пароль!'
        else:
            user = User.objects.create_user(
                username=_username,
                email=_email,
                password=_password1,
            )
            user.save()

            return HttpResponseRedirect(reverse('accounts:login'))

    context = {'message': message,
               'title': title}
    return render(request, template, context)


def logout(request):
    user_logout(request)
    return HttpResponseRedirect(reverse('home'))


class ProfileDetailView(DetailView):
    model = Profile
    context_object_name = 'profile'
    template_name = 'accounts/profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль {} | CSOL'.format(context['object'])
        context['user_id'] = self.kwargs['user_id']
        return context

    def get_object(self):
        _user = get_object_or_404(User, pk=int(self.kwargs['user_id']))
        return get_object_or_404(Profile, user=_user)


def profile_edit(request):
    template = 'accounts/profile_edit.html'
    title = 'Мой профиль | CSOL'

    if request.method == 'POST':
        print(request.FILES)
        _website = request.POST['website']
        _email = request.POST['email']
        _lastname = request.POST['last_name']
        _firstname = request.POST['first_name']
        _date_birth = request.POST['date_birth']
        _photo = request.FILES['photo']
        print(_photo)

        fs = FileSystemStorage()
        filename = fs.save(_photo.name, _photo)
        uploaded_file_url = fs.url(filename)

        user = request.user
        profile = Profile.objects.get(user=user)

        user.last_name = _lastname
        user.first_name = _firstname
        user.email = _email

        profile.site = _website
        profile.photo = uploaded_file_url
        profile.date_of_birth = _date_birth

        user.save()
        profile.save()

        return HttpResponseRedirect(reverse('accounts:profile', args=[request.user.id]))

    context = {'title': title}
    return render(request, template, context)
