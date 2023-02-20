from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from core.models import *
# Create your views here.


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("/")

        else:
            return HttpResponse("Not correct")
    return render(request, "core/login.html")


def user_register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email_address = request.POST["email_address"]
        password = request.POST["password"]

        new_user = Customer(username=username, email=email_address)
        new_user.set_password(str(password))

        new_user.save()
        login(request, new_user)
        return redirect("/")

    return render(request, "core/login.html")


def user_logout(request):
    logout(request)
    return redirect("user_login")
