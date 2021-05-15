from django.contrib.auth import (login as auth_login, authenticate)
from django.contrib.auth import logout as user_logout
from django.contrib.auth.models import User

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def login(request):
    template = 'registration/login.html'

    _message = None
    _title = 'Авторизация | CSOL'
    if request.method == 'POST':
        _username = request.POST['username']
        _password = request.POST['password']
        user = authenticate(username=_username, password=_password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                _message = 'Ваш аккаунт не активирован!'
        else:
            _message = 'Неправильно введен логин или пароль.'
    context = {'message': _message,
               'title': _title}
    return render(request, template, context)


def register(request):
    template = 'registration/register.html'

    _message = None
    _title = 'Регистрация | CSOL'

    if request.method == 'POST':
        _username = request.POST['username']
        _email = request.POST['email']
        _password1 = request.POST['password1']
        _password2 = request.POST['password2']

        if User.objects.filter(username=_username).exists():
            _message = 'Такой пользователь уже существует!'
        elif _password1 != _password2:
            _message = 'Неправильно введен повторный пароль!'
        else:
            user = User.objects.create_user(
                username=_username,
                email=_email,
                password=_password1,
            )
            user.save()

            return HttpResponseRedirect(reverse('accounts:login'))

    context = {'message': _message,
               'title': _title}
    return render(request, template, context)


def logout(request):
    user_logout(request)
    return HttpResponseRedirect(reverse('home'))
