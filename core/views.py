from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from core.forms import *

# Create your views here.


def index(request):
    return render(request, 'core/index.html')


def checkout(request):
    return render(request, 'core/checkout.html')


def cart(request):
    return render(request, 'core/cart.html')
