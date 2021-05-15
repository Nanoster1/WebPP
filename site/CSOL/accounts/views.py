from django.contrib.auth import (login as auth_login, authenticate)
from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse


def login(request):
    template = 'registration/login.html'

    _message = None
    if request.method == 'POST':
        _username = request.POST['username']
        _password = request.POST['password']
        user = authenticate(username=_username, password=_password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                _message = 'Your account is not activated'
        else:
            _message = 'Invalid login, please try again.'
    context = {'message': _message}
    return render(request, template, context)


def register(request):
    template = 'registration/register.html'

    _message = None

    if request.method == 'POST':
        _username = request.POST['username']
        _password1 = request.POST['password1']
        _password2 = request.POST['password2']

        if User.objects.filter(username=_username).exists():
            _message = 'Username already exists.'
        elif _password1 != _password2:
            _message = 'Passwords do not match.'
        else:
            # Create the user:
            user = User.objects.create_user(
                username=_username,
                email=None,
                password=_password1,
            )
            user.save()

            return HttpResponseRedirect(reverse('accounts:*login'))

    context = {'message': _message}
    return render(request, template, context)
