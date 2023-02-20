from django.shortcuts import render
from django.contrib.auth.models import User
from core.models import *
# Create your views here.


def user_login(request):
    return render(request, "core/login.html")


def user_register(request):
    pass


def user_logout(request):
    pass
